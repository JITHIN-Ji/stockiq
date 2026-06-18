"""
StockIQ Insight Generator
Uses Anthropic Claude to generate narrative insights.
ONLY called during admin data ingestion — never during page loads.
"""

import os
import json
import re
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



def generate_business_canvas(company_id: int) -> bool:
    """
    Generate Business Model Canvas (9 boxes) describing how the COMPANY
    operates — not how to invest in the stock. One Gemini call, JSON
    response, parsed into 9 fields. Returns True on success.
    """
    from app import db
    from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, BusinessCanvas

    company = Company.query.get(company_id)
    if not company:
        return False

    growth         = GrowthMetrics.query.filter_by(company_id=company_id).first()
    quality        = QualityMetrics.query.filter_by(company_id=company_id).first()
    shareholding   = Shareholding.query.filter_by(company_id=company_id).first()
    classification = Classification.query.filter_by(company_id=company_id).first()

    ctx = _build_company_context(company, growth, quality, shareholding, classification)

    prompt = (
        "You are a business analyst. Given the data below about "
        f"{company.name} (sector: {company.sector or 'N/A'}), produce a "
        "Business Model Canvas describing how the COMPANY operates "
        "(not investment advice about its stock).\n\n"
        "Return ONLY valid JSON. No markdown. No code fences. No preamble. "
        "Exactly these 9 keys, each a string of 20-40 words, plain English:\n\n"
        "1. KEY PARTNERS: Strategic companies/people the business works with. "
        "Include: resources received, activities performed by partners, motivations for partnership, dependency level.\n\n"
        "2. KEY ACTIVITIES: Specific tasks fundamental to operation. Include: activities to deliver value, "
        "what sets company apart, how they differ from competitors, niche resources needed, cost optimization.\n\n"
        "3. KEY RESOURCES: Assets necessary to operate and deliver value proposition. "
        "Include: specific assets needed, resources for distribution/revenue/customer relationships, capital/human resource needs.\n\n"
        "4. VALUE PROPOSITIONS: The primary offering and mission (most important element). "
        "Include: mission/vision, what is offered to customers, problems solved, needs satisfied, differentiation.\n\n"
        "5. CUSTOMER RELATIONSHIPS: Types of interactions with customers. "
        "Include: importance of relationships, relationship type (dedicated vs self-serve), differences by segment, communication frequency, support level.\n\n"
        "6. CHANNELS: Structures and methods to deliver product/value to customers. "
        "Include: how channels deliver value, how to reach customer segments, integration/efficiency, effectiveness.\n\n"
        "7. CUSTOMER SEGMENTS: Different types of customers managed. "
        "Include: main focus, most important customers, characteristics/needs/preferences, different customer types, market focus (niche vs mass).\n\n"
        "8. COST STRUCTURE: How company spends money on operations and key costs. "
        "Include: major cost drivers, how activities/resources contribute to costs, relationship to revenue, economies of scale, fixed vs variable costs, cost optimization vs value focus.\n\n"
        "9. REVENUE STREAMS: Sources of cash flows and how value generates money. "
        "Include: multiple revenue methods, pricing strategy, payment channels, multiple payment forms (upfront, plans, financing).\n\n"
        "{\n"
        '  "key_partners": "...",\n'
        '  "key_activities": "...",\n'
        '  "key_resources": "...",\n'
        '  "value_propositions": "...",\n'
        '  "customer_relationships": "...",\n'
        '  "channels": "...",\n'
        '  "customer_segments": "...",\n'
        '  "cost_structure": "...",\n'
        '  "revenue_streams": "..."\n'
        "}\n\n"
        f"Company data:\n{ctx}"
    )

    raw = _call_anthropic(prompt, max_tokens=900)
    cleaned = re.sub(r"^```json|```$", "", raw.strip(), flags=re.MULTILINE).strip()

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return False

    required = [
        "key_partners", "key_activities", "key_resources", "value_propositions",
        "customer_relationships", "channels", "customer_segments",
        "cost_structure", "revenue_streams",
    ]
    if not all(k in data for k in required):
        return False

    canvas = BusinessCanvas.query.filter_by(company_id=company_id).first()
    if not canvas:
        canvas = BusinessCanvas(company_id=company_id)
        db.session.add(canvas)

    for k in required:
        setattr(canvas, k, data[k])
    canvas.generated_at = datetime.utcnow()

    db.session.commit()
    return True