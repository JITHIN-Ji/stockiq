"""
StockIQ Classification Engine
Rule-based classification of stocks into Peter Lynch buckets.
No AI is used here — pure financial logic.
"""

import json
from dataclasses import dataclass, field
from typing import Optional


# ── Bucket names ──────────────────────────────────────────────────────────────
SLOW_MOVER  = "Slow Mover"
STALWART    = "Stalwart"
FAST_GROWER = "Fast Grower"
CYCLICAL    = "Cyclical"
TURNAROUND  = "Turnaround"
ASSET_PLAY  = "Asset Play"

CYCLICAL_SECTORS = {
    "steel", "metals", "mining", "power", "energy",
    "auto", "automobile", "oil", "gas", "cement",
    "chemicals", "commodities", "fertilizers"
}

CYCLICAL_INDUSTRIES = {
    "steel", "aluminium", "copper", "zinc", "iron ore",
    "thermal power", "solar power", "crude oil", "natural gas",
    "auto components", "tyres", "cement", "specialty chemicals",
    "oil refining", "petrochemicals", "diversified metals"
}


@dataclass
class ClassificationResult:
    primary_bucket: str
    confidence_score: float
    reasoning: list = field(default_factory=list)


def classify_company(company, growth, quality, shareholding=None) -> ClassificationResult:
    """
    Classify a company into a Peter Lynch bucket based on financial metrics.
    Returns a ClassificationResult with bucket, confidence, and reasoning.
    """
    scores = {
        SLOW_MOVER:  0,
        STALWART:    0,
        FAST_GROWER: 0,
        CYCLICAL:    0,
        TURNAROUND:  0,
        ASSET_PLAY:  0,
    }
    reasoning = []

    sector_lower   = (company.sector   or "").lower()
    industry_lower = (company.industry or "").lower()

    is_cyclical_sector = (
        any(kw in sector_lower   for kw in CYCLICAL_SECTORS) or
        any(kw in industry_lower for kw in CYCLICAL_INDUSTRIES)
    )

    # ── Step 1: Cyclical sector flag (highest priority) ────────────────────────
    if is_cyclical_sector:
        scores[CYCLICAL] += 40
        reasoning.append(
            f"Operates in a cyclical sector ({company.sector}), "
            "with earnings closely tied to commodity/economic cycles."
        )

    # ── Step 2: Growth-based scoring ──────────────────────────────────────────
    if growth:
        profit_1y = growth.profit_growth_1y or 0
        profit_3y = growth.profit_growth_3y or 0
        sales_1y  = growth.sales_growth_1y  or 0
        sales_3y  = growth.sales_growth_3y  or 0
        sales_5y  = growth.sales_growth_5y  or 0
        profit_5y = growth.profit_growth_5y or 0

        # Turnaround: big jump in recent profits from a low base
        if profit_1y > 30 and profit_3y < 10:
            scores[TURNAROUND] += 30
            reasoning.append(
                f"Profit growth jumped to {profit_1y:.1f}% (1Y) vs {profit_3y:.1f}% (3Y CAGR), "
                "suggesting a business in recovery."
            )

        # Fast Grower: high sustained growth
        if sales_5y > 20 and profit_5y > 20:
            scores[FAST_GROWER] += 40
            reasoning.append(
                f"Exceptional 5-year CAGR: revenue {sales_5y:.1f}%, profit {profit_5y:.1f}% "
                "— hallmarks of a fast grower."
            )
        elif sales_3y > 15 and profit_1y > 15:
            scores[FAST_GROWER] += 25
            reasoning.append(
                f"Strong recent growth: revenue 3Y CAGR {sales_3y:.1f}%, "
                f"profit {profit_1y:.1f}%."
            )

        # Stalwart: moderate, consistent growth (NOT for cyclicals)
        if not is_cyclical_sector:
            if 8 <= sales_5y <= 20 and profit_5y > 5:
                scores[STALWART] += 30
                reasoning.append(
                    f"Steady 5Y revenue CAGR of {sales_5y:.1f}% with consistent "
                    "profitability — classic stalwart profile."
                )
            elif 6 <= sales_3y <= 18:
                scores[STALWART] += 15

        # Slow Mover: low growth
        if sales_5y < 4 and sales_3y < 4:
            scores[SLOW_MOVER] += 35
            reasoning.append(
                f"Revenue growth of {sales_5y:.1f}% (5Y) and {sales_3y:.1f}% (3Y) "
                "indicates a slow-growth, mature business."
            )
        elif sales_5y < 8:
            scores[SLOW_MOVER] += 10

    # ── Step 3: Balance sheet quality ─────────────────────────────────────────
    if quality:
        de = quality.debt_to_equity or 0

        if de < 0.3:
            if not is_cyclical_sector:
                scores[STALWART]    += 10
                scores[FAST_GROWER] += 5
            reasoning.append(
                f"Low debt-to-equity ({de:.2f}x) reflects a very strong balance sheet."
            )
        elif de > 1.5:
            scores[TURNAROUND] += 15
            reasoning.append(
                f"High debt ({de:.2f}x D/E) — leverage is a key risk to monitor."
            )
            # Extra penalty in cyclical sector
            if is_cyclical_sector:
                scores[CYCLICAL]   += 10
                scores[TURNAROUND] += 10
                reasoning.append(
                    "Elevated leverage in a cyclical sector amplifies earnings volatility."
                )

        if quality.roe and quality.roe > 20 and not is_cyclical_sector:
            scores[STALWART]    += 10
            scores[FAST_GROWER] += 10
            reasoning.append(
                f"ROE of {quality.roe:.1f}% exceeds 20%, "
                "indicating excellent capital efficiency."
            )

        if quality.interest_coverage and quality.interest_coverage < 2:
            scores[TURNAROUND] += 15
            reasoning.append(
                f"Interest coverage of {quality.interest_coverage:.1f}x is very low "
                "— cash flows barely cover interest payments."
            )

    # ── Step 4: Dividend / income signals ─────────────────────────────────────
    if company.dividend_yield and company.dividend_yield > 1.5:
        scores[SLOW_MOVER] += 15
        reasoning.append(
            f"Dividend yield of {company.dividend_yield:.2f}% is above average, "
            "typical of mature income-generating businesses."
        )

    # ── Step 5: Market cap (only for non-cyclical) ─────────────────────────────
    if company.market_cap and not is_cyclical_sector:
        if company.market_cap > 100000:
            scores[STALWART] += 15
            reasoning.append(
                f"Large-cap company (₹{company.market_cap:,.0f} Cr) with "
                "institutional-grade scale and stability."
            )
        elif company.market_cap < 10000:
            scores[FAST_GROWER] += 10

    # ── Step 6: Asset Play signals ─────────────────────────────────────────────
    if company.pb_ratio and company.pb_ratio < 1.2:
        scores[ASSET_PLAY] += 20
        reasoning.append(
            f"P/B of {company.pb_ratio:.2f}x — stock trades near or below book value."
        )
    if is_cyclical_sector and company.pb_ratio and company.pb_ratio < 1.5:
        scores[ASSET_PLAY] += 12

    # ── Conglomerate special case (Reliance) ────────────────────────────────────
    if "conglomerate" in sector_lower:
        scores[CYCLICAL]  = max(0, scores[CYCLICAL] - 20)
        scores[STALWART] += 20

    # ── Select winner ──────────────────────────────────────────────────────────
    best_bucket = max(scores, key=scores.get)
    raw_score   = scores[best_bucket]
    total       = sum(scores.values()) or 1
    confidence  = round(min((raw_score / total) * 200, 95), 1)

    if not reasoning:
        reasoning.append(
            f"Classified as {best_bucket} based on overall financial profile."
        )

    return ClassificationResult(
        primary_bucket=best_bucket,
        confidence_score=confidence,
        reasoning=reasoning[:5],
    )


def classify_and_save(company_id: int):
    """
    Classify a company and persist the result to the database.
    Returns the saved Classification object or None on error.
    """
    from app import db
    from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification

    company     = Company.query.get(company_id)
    if not company:
        return None

    growth      = GrowthMetrics.query.filter_by(company_id=company_id).first()
    quality     = QualityMetrics.query.filter_by(company_id=company_id).first()
    shareholding = Shareholding.query.filter_by(company_id=company_id).first()

    result = classify_company(company, growth, quality, shareholding)

    clf = Classification.query.filter_by(company_id=company_id).first()
    if not clf:
        clf = Classification(company_id=company_id)
        db.session.add(clf)

    clf.primary_bucket    = result.primary_bucket
    clf.confidence_score  = result.confidence_score
    clf.reasoning_json    = json.dumps(result.reasoning)
    from datetime import datetime
    clf.last_updated = datetime.utcnow()
    db.session.commit()
    return clf
