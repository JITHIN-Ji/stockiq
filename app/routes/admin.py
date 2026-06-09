"""
StockIQ Admin Routes
Endpoints for data ingestion, classification, and insight generation.
Protected by a simple token for MVP.
"""

import os
from flask import Blueprint, jsonify, request
from app import db
from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, Insights
from app.services.classifier import classify_and_save
from app.services.insight_generator import generate_insights

admin_bp = Blueprint("admin", __name__)

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "stockiq-admin-secret")


def _require_token():
    token = request.headers.get("X-Admin-Token") or request.args.get("token")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    return None


@admin_bp.route("/classify", methods=["POST"])
def run_classification():
    """Run classification engine for all (or one) company."""
    auth = _require_token()
    if auth:
        return auth

    data = request.get_json() or {}
    company_id = data.get("company_id")

    if company_id:
        clf = classify_and_save(company_id)
        if not clf:
            return jsonify({"error": "Company not found"}), 404
        return jsonify({"success": True, "company_id": company_id, "bucket": clf.primary_bucket})

    # Classify all
    companies = Company.query.all()
    results = []
    for c in companies:
        clf = classify_and_save(c.id)
        if clf:
            results.append({"company_id": c.id, "name": c.name, "bucket": clf.primary_bucket})

    return jsonify({"success": True, "classified": results})


@admin_bp.route("/generate-insights", methods=["POST"])
def run_insight_generation():
    """Generate AI insights for all (or one) company."""
    auth = _require_token()
    if auth:
        return auth

    data = request.get_json() or {}
    company_id = data.get("company_id")

    if company_id:
        ok = generate_insights(company_id)
        return jsonify({"success": ok, "company_id": company_id})

    companies = Company.query.all()
    results = []
    for c in companies:
        ok = generate_insights(c.id)
        results.append({"company_id": c.id, "name": c.name, "success": ok})

    return jsonify({"success": True, "results": results})


@admin_bp.route("/seed", methods=["POST"])
def seed_database():
    """
    Seed the database with the 10 MVP stocks.
    Safe to call multiple times — uses upsert logic.
    """
    auth = _require_token()
    if auth:
        return auth

    from scripts.seed_data import SEED_DATA, seed_company
    created, updated = 0, 0
    for record in SEED_DATA:
        is_new = seed_company(record)
        if is_new:
            created += 1
        else:
            updated += 1

    return jsonify({"success": True, "created": created, "updated": updated})


@admin_bp.route("/status", methods=["GET"])
def status():
    """Check data completeness for all companies."""
    auth = _require_token()
    if auth:
        return auth

    companies = Company.query.all()
    report = []
    for c in companies:
        report.append({
            "id": c.id,
            "ticker": c.ticker,
            "name": c.name,
            "has_growth": GrowthMetrics.query.filter_by(company_id=c.id).count() > 0,
            "has_quality": QualityMetrics.query.filter_by(company_id=c.id).count() > 0,
            "has_shareholding": Shareholding.query.filter_by(company_id=c.id).count() > 0,
            "has_classification": Classification.query.filter_by(company_id=c.id).count() > 0,
            "has_insights": Insights.query.filter_by(company_id=c.id).count() > 0,
        })
    return jsonify(report)
