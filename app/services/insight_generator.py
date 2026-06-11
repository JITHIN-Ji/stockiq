"""
StockIQ Insight Generator
Uses Anthropic Claude to generate narrative insights.
ONLY called during admin data ingestion — never during page loads.
"""

import os
import json
from datetime import datetime
from pathlib import Path


def _call_anthropic(prompt: str, max_tokens: int = 1024) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    return response.text.strip()


def _build_company_context(company, growth, quality, shareholding, classification) -> str:
    """Build a compact financial context string for LLM prompts."""
    lines = [
        f"Company: {company.name}",
        f"Sector: {company.sector} | Industry: {company.industry}",
        f"Market Cap: ₹{company.market_cap:,.0f} Cr" if company.market_cap else "",
        f"Current Price: ₹{company.current_price}" if company.current_price else "",
        f"P/E: {company.pe_ratio} | P/B: {company.pb_ratio}" if company.pe_ratio else "",
        f"Dividend Yield: {company.dividend_yield}%" if company.dividend_yield else "",
    ]

    if growth:
        lines += [
            f"Revenue Growth: 1Y={growth.sales_growth_1y}%, 3Y={growth.sales_growth_3y}%, 5Y={growth.sales_growth_5y}%",
            f"Profit Growth:  1Y={growth.profit_growth_1y}%, 3Y={growth.profit_growth_3y}%, 5Y={growth.profit_growth_5y}%",
        ]

    if quality:
        lines += [
            f"ROE: {quality.roe}% | ROCE: {quality.roce}%",
            f"Debt/Equity: {quality.debt_to_equity}x | Interest Coverage: {quality.interest_coverage}x",
            f"Profit Margin: {quality.profit_margin}%",
        ]

    if shareholding:
        lines.append(
            f"Shareholding: Promoter {shareholding.promoter_holding}%, "
            f"FII {shareholding.fii_holding}%, DII {shareholding.dii_holding}%"
        )

    if classification:
        lines.append(f"Classification: {classification.primary_bucket} ({classification.confidence_score}% confidence)")

    return "\n".join(l for l in lines if l)


def generate_insights(company_id: int) -> bool:
    """
    Generate all AI narrative sections for a company and save to DB.
    Returns True on success, False on failure.
    """
    from app import db
    from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, Insights

    company = Company.query.get(company_id)
    if not company:
        return False

    growth         = GrowthMetrics.query.filter_by(company_id=company_id).first()
    quality        = QualityMetrics.query.filter_by(company_id=company_id).first()
    shareholding   = Shareholding.query.filter_by(company_id=company_id).first()
    classification = Classification.query.filter_by(company_id=company_id).first()

    ctx = _build_company_context(company, growth, quality, shareholding, classification)
    bucket = classification.primary_bucket if classification else "Unknown"

    
    prompts_file = Path("data/prompts.json")
    try:
        prompts = json.loads(prompts_file.read_text()) if prompts_file.exists() else {}
    except Exception:
        prompts = {}

    def _render(key, fallback):
        """Use saved prompt if exists, else use fallback. Fill placeholders."""
        tpl = prompts.get(key) or fallback
        return tpl.format(
            company_name=company.name,
            sector=company.sector or "",
            bucket=bucket,
            financial_context=ctx,
        )

    # ── About Company ──────────────────────────────────────────────────────────
    about = _call_anthropic(_render("about",
        "You are a financial analyst writing for retail investors in India.\n"
        "Given the following data about {company_name}, write a concise 'About the Company' section in 100–150 words.\n"
        "Focus on: what the company does, its market position, and key business segments.\n"
        "Write in plain English. No bullet points. No markdown. No jargon.\n\n"
        "{financial_context}"
    ))

    # ── Future Scope ───────────────────────────────────────────────────────────
    future = _call_anthropic(_render("future",
        "You are a financial analyst writing for retail investors in India.\n"
        "Given the following data about {company_name}, write a 'Future Scope' section in 100–150 words.\n"
        "Focus on: industry tailwinds, expansion opportunities, and growth levers.\n"
        "Write in plain English. No bullet points. No markdown. Be realistic.\n\n"
        "{financial_context}"
    ))

    # ── Risks ──────────────────────────────────────────────────────────────────
    risks = _call_anthropic(_render("risks",
        "You are a financial analyst writing for retail investors in India.\n"
        "Given the following data about {company_name}, write a 'Key Risks' section in 100–150 words.\n"
        "Focus on: debt risk, competition, sector headwinds, and company-specific concerns.\n"
        "Write in plain English. No bullet points. No markdown. Be honest.\n\n"
        "{financial_context}"
    ))

    # ── Investment Thesis ──────────────────────────────────────────────────────
    thesis = _call_anthropic(_render("thesis",
        "You are a financial analyst writing for retail investors in India.\n"
        "{company_name} has been classified as a '{bucket}' stock.\n"
        "Write a 100–150 word 'Investment Thesis' explaining why this classification fits.\n"
        "Relate the thesis to actual metrics. Write in plain English. No bullet points. No markdown.\n\n"
        "{financial_context}"
    ))

    # ── Save ───────────────────────────────────────────────────────────────────
    insight = Insights.query.filter_by(company_id=company_id).first()
    if not insight:
        insight = Insights(company_id=company_id)
        db.session.add(insight)

    insight.about_company     = about
    insight.future_scope      = future
    insight.risks             = risks
    insight.investment_thesis = thesis
    insight.generated_at      = datetime.utcnow()
    db.session.commit()
    return True