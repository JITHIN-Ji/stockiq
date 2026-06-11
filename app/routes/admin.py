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


import json
from pathlib import Path


def _require_token():
    token = request.headers.get("X-Admin-Token") or request.args.get("token")
    if token != ADMIN_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401
    return None


PROMPTS_FILE = Path("data/prompts.json")

PROMPT_DEFAULTS = {
    "about": """You are a financial analyst writing for retail investors in India.
Given the following data about {company_name}, write a concise 'About the Company' section in 100–150 words.
Focus on: what the company does, its market position, and key business segments.
Write in plain English. No bullet points. No markdown. No jargon.

{financial_context}""",

    "future": """You are a financial analyst writing for retail investors in India.
Given the following data about {company_name}, write a 'Future Scope' section in 100–150 words.
Focus on: industry tailwinds, expansion opportunities, and growth levers.
Write in plain English. No bullet points. No markdown. Be realistic.

{financial_context}""",

    "risks": """You are a financial analyst writing for retail investors in India.
Given the following data about {company_name}, write a 'Key Risks' section in 100–150 words.
Focus on: debt risk, competition, sector headwinds, and company-specific concerns.
Write in plain English. No bullet points. No markdown. Be honest.

{financial_context}""",

    "thesis": """You are a financial analyst writing for retail investors in India.
{company_name} has been classified as a '{bucket}' stock.
Write a 100–150 word 'Investment Thesis' explaining why this classification fits.
Relate the thesis to actual metrics. Write in plain English. No bullet points. No markdown.

{financial_context}""",
}


def _load_prompts() -> dict:
    """Read prompts.json. Fall back to defaults if missing/corrupt."""
    if PROMPTS_FILE.exists():
        try:
            return json.loads(PROMPTS_FILE.read_text())
        except Exception:
            pass
    return dict(PROMPT_DEFAULTS)


def _save_prompts(data: dict):
    """Write prompts dict to data/prompts.json."""
    PROMPTS_FILE.parent.mkdir(exist_ok=True)
    PROMPTS_FILE.write_text(json.dumps(data, indent=2))


@admin_bp.route("/prompts", methods=["GET"])
def get_prompts():
    """Return current prompts (saved or defaults)."""
    auth = _require_token()
    if auth: return auth
    return jsonify(_load_prompts())


@admin_bp.route("/prompts", methods=["POST"])
def save_prompts():
    """Save edited prompts to data/prompts.json."""
    auth = _require_token()
    if auth: return auth
    data = request.get_json() or {}
    prompts = _load_prompts()
    for k in PROMPT_DEFAULTS:        # only save known keys
        if k in data:
            prompts[k] = data[k]
    _save_prompts(prompts)
    return jsonify({"success": True})


@admin_bp.route("/scrape", methods=["POST"])
def scrape_single():
    """Scrape one ticker → save to DB → return company_id."""
    auth = _require_token()
    if auth: return auth

    data       = request.get_json() or {}
    ticker     = (data.get("ticker") or "").strip().upper()
    slug       = (data.get("screener_slug") or ticker).strip().upper()

    if not ticker:
        return jsonify({"success": False, "error": "ticker required"}), 400

    # Block duplicate
    existing = Company.query.filter_by(ticker=ticker).first()
    if existing:
        return jsonify({"success": False, "error": f"{ticker} already in DB"}), 409

    try:
        from scripts.scraper_screener import scrape_ticker, SCREENER_SLUG
        SCREENER_SLUG[ticker] = slug          # inject custom slug if provided
        scraped = scrape_ticker(ticker)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    if not scraped:
        return jsonify({"success": False, "error": f"No data returned for {ticker}"}), 500

    try:
        from scripts.fetch_and_seed import save_company
        company_id = save_company(db, scraped)
        if not company_id:
            return jsonify({"success": False, "error": "DB save failed"}), 500
        return jsonify({"success": True, "company_id": company_id, "ticker": ticker})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@admin_bp.route("/company-insights/<int:company_id>", methods=["GET"])
def get_company_insights(company_id):
    """Return saved insights JSON for modal display."""
    auth = _require_token()
    if auth: return auth

    ins = Insights.query.filter_by(company_id=company_id).first()
    if not ins:
        return jsonify({"error": "No insights found"}), 404

    return jsonify({
        "about_company":     ins.about_company,
        "future_scope":      ins.future_scope,
        "risks":             ins.risks,
        "investment_thesis": ins.investment_thesis,
    })


@admin_bp.route("/company/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    """Delete company + all related rows (cascade manual)."""
    auth = _require_token()
    if auth: return auth

    company = Company.query.get(company_id)
    if not company:
        return jsonify({"error": "Not found"}), 404

    # Delete child rows first — no FK cascade in SQLite by default
    GrowthMetrics.query.filter_by(company_id=company_id).delete()
    QualityMetrics.query.filter_by(company_id=company_id).delete()
    Shareholding.query.filter_by(company_id=company_id).delete()
    Classification.query.filter_by(company_id=company_id).delete()
    Insights.query.filter_by(company_id=company_id).delete()
    db.session.delete(company)
    db.session.commit()

    return jsonify({"success": True, "deleted": company_id})




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
