"""
StockIQ API Routes
RESTful JSON API for stock data.
"""

from flask import Blueprint, jsonify, request
from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, Insights
from app.services.question_engine import generate_qa

api_bp = Blueprint("api", __name__)


@api_bp.route("/stocks", methods=["GET"])
def get_all_stocks():
    """Return all companies with basic info."""
    companies = Company.query.order_by(Company.market_cap.desc()).all()
    return jsonify([c.to_dict() for c in companies])


@api_bp.route("/stocks/<int:company_id>", methods=["GET"])
def get_stock(company_id):
    """Return full data for a single company."""
    company = Company.query.get_or_404(company_id)
    growth = GrowthMetrics.query.filter_by(company_id=company_id).first()
    quality = QualityMetrics.query.filter_by(company_id=company_id).first()
    shareholding = Shareholding.query.filter_by(company_id=company_id).first()
    classification = Classification.query.filter_by(company_id=company_id).first()
    insights = Insights.query.filter_by(company_id=company_id).first()
    qa_pairs = generate_qa(company, growth, quality, shareholding, classification)

    return jsonify({
        "company": company.to_dict(),
        "growth_metrics": growth.to_dict() if growth else None,
        "quality_metrics": quality.to_dict() if quality else None,
        "shareholding": shareholding.to_dict() if shareholding else None,
        "classification": classification.to_dict() if classification else None,
        "insights": insights.to_dict() if insights else None,
        "qa": qa_pairs,
    })


@api_bp.route("/search", methods=["GET"])
def search_stocks():
    """Search companies by name or ticker."""
    q = request.args.get("q", "").strip()
    if len(q) < 1:
        return jsonify([])

    results = Company.query.filter(
        (Company.name.ilike(f"%{q}%")) | (Company.ticker.ilike(f"%{q}%"))
    ).order_by(Company.market_cap.desc()).limit(10).all()

    return jsonify([
        {"id": c.id, "ticker": c.ticker, "name": c.name, "sector": c.sector}
        for c in results
    ])
