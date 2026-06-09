"""
StockIQ Main Routes
Handles frontend page rendering.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, Insights
from app.services.question_engine import generate_qa

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Home page with search and popular stocks."""
    popular = Company.query.order_by(Company.market_cap.desc()).limit(6).all()
    return render_template("index.html", popular_stocks=popular)


@main_bp.route("/stock/<ticker>")
def stock_detail(ticker):
    """Stock detail page — all data served from DB, no runtime AI."""
    company = Company.query.filter_by(ticker=ticker.upper()).first_or_404()

    growth = GrowthMetrics.query.filter_by(company_id=company.id).first()
    quality = QualityMetrics.query.filter_by(company_id=company.id).first()
    shareholding = Shareholding.query.filter_by(company_id=company.id).first()
    classification = Classification.query.filter_by(company_id=company.id).first()
    insights = Insights.query.filter_by(company_id=company.id).first()

    qa_pairs = generate_qa(company, growth, quality, shareholding, classification)

    return render_template(
        "stock_detail.html",
        company=company,
        growth=growth,
        quality=quality,
        shareholding=shareholding,
        classification=classification,
        insights=insights,
        qa_pairs=qa_pairs,
    )


@main_bp.route("/search")
def search():
    """Search redirect — handles GET form submission."""
    q = request.args.get("q", "").strip()
    if not q:
        return redirect(url_for("main.index"))

    # Try exact ticker match first
    company = Company.query.filter(
        Company.ticker.ilike(q)
    ).first()

    if not company:
        company = Company.query.filter(
            Company.name.ilike(f"%{q}%")
        ).first()

    if company:
        return redirect(url_for("main.stock_detail", ticker=company.ticker))

    # No match — return to home with message
    popular = Company.query.order_by(Company.market_cap.desc()).limit(6).all()
    return render_template(
        "index.html",
        popular_stocks=popular,
        search_query=q,
        no_results=True,
    )
