"""
StockIQ Question Engine
Maps predefined investor questions to structured database values.
NO AI is used here — pure data retrieval.
"""


def _fmt_crore(val):
    if val is None:
        return "N/A"
    if val >= 100000:
        return f"₹{val / 100000:.2f} Lakh Crore"
    return f"₹{val:,.0f} Crore"


def _fmt_pct(val, suffix="%"):
    if val is None:
        return "N/A"
    return f"{val:.2f}{suffix}"


def _fmt_ratio(val, decimals=2):
    if val is None:
        return "N/A"
    return f"{val:.{decimals}f}x"


def generate_qa(company, growth, quality, shareholding, classification):
    """
    Generate all predefined Q&A pairs from structured data.
    Returns a list of {question, answer, category} dicts.
    """
    qa = []

    # ── Valuation ──────────────────────────────────────────────────────────────
    qa.append({
        "category": "Valuation",
        "question": "What is the current valuation of the company?",
        "answer": (
            f"{company.name} trades at a P/E of {_fmt_ratio(company.pe_ratio, 1)} "
            f"and a P/B of {_fmt_ratio(company.pb_ratio, 2)}. "
            f"The stock is currently priced at ₹{company.current_price:,.2f}."
            if company.current_price else "Valuation data not available."
        ),
    })

    qa.append({
        "category": "Valuation",
        "question": "What is the market capitalization?",
        "answer": f"{company.name} has a market cap of {_fmt_crore(company.market_cap)}.",
    })

    qa.append({
        "category": "Valuation",
        "question": "What is the P/E ratio?",
        "answer": (
            f"The price-to-earnings ratio is {_fmt_ratio(company.pe_ratio, 1)}. "
            + (_pe_interpretation(company.pe_ratio))
        ),
    })

    # ── Growth ─────────────────────────────────────────────────────────────────
    if growth:
        qa.append({
            "category": "Growth",
            "question": "What is the revenue growth rate?",
            "answer": (
                f"{company.name} has grown revenue at {_fmt_pct(growth.sales_growth_1y)} (1Y), "
                f"{_fmt_pct(growth.sales_growth_3y)} CAGR (3Y), and "
                f"{_fmt_pct(growth.sales_growth_5y)} CAGR (5Y)."
            ),
        })

        qa.append({
            "category": "Growth",
            "question": "What is the profit growth rate?",
            "answer": (
                f"Net profit has grown at {_fmt_pct(growth.profit_growth_1y)} (1Y), "
                f"{_fmt_pct(growth.profit_growth_3y)} CAGR (3Y), and "
                f"{_fmt_pct(growth.profit_growth_5y)} CAGR (5Y)."
            ),
        })

        qa.append({
            "category": "Growth",
            "question": "For how long has the company maintained growth?",
            "answer": _growth_consistency(growth),
        })

        qa.append({
            "category": "Growth",
            "question": "How does the company growth compare with India GDP growth?",
            "answer": _vs_gdp(growth),
        })

    # ── Industry ───────────────────────────────────────────────────────────────
    qa.append({
        "category": "Industry",
        "question": "What type of industry does the company operate in?",
        "answer": (
            f"{company.name} operates in the {company.industry} industry "
            f"within the {company.sector} sector."
        ),
    })

    if company.listing_year:
        age = 2025 - company.listing_year
        qa.append({
            "category": "Industry",
            "question": "How old is the company?",
            "answer": (
                f"{company.name} has been listed since {company.listing_year}, "
                f"making it approximately {age} years old as a publicly listed entity."
            ),
        })

    # ── Dividends ──────────────────────────────────────────────────────────────
    qa.append({
        "category": "Dividends",
        "question": "Does the company pay dividends?",
        "answer": _dividend_answer(company),
    })

    # ── Quality ────────────────────────────────────────────────────────────────
    if quality:
        qa.append({
            "category": "Quality",
            "question": "What is the return on equity (ROE)?",
            "answer": (
                f"ROE stands at {_fmt_pct(quality.roe)}, "
                + _roe_interpretation(quality.roe)
            ),
        })

        qa.append({
            "category": "Quality",
            "question": "How is the company's debt situation?",
            "answer": _debt_answer(company, quality),
        })

        qa.append({
            "category": "Quality",
            "question": "How does the company behave during recessions?",
            "answer": _recession_behavior(company, quality),
        })

    # ── Shareholding ───────────────────────────────────────────────────────────
    if shareholding:
        qa.append({
            "category": "Ownership",
            "question": "Who are the major shareholders?",
            "answer": (
                f"Promoters hold {_fmt_pct(shareholding.promoter_holding)}, "
                f"FIIs {_fmt_pct(shareholding.fii_holding)}, "
                f"DIIs {_fmt_pct(shareholding.dii_holding)}, "
                f"and public {_fmt_pct(shareholding.public_holding)} "
                f"(as of {shareholding.as_of_date or 'latest quarter'})."
            ),
        })

    # ── Classification ─────────────────────────────────────────────────────────
    if classification:
        qa.append({
            "category": "Classification",
            "question": "What kind of stock is this?",
            "answer": (
                f"{company.name} is classified as a {classification.primary_bucket} "
                f"with a confidence of {classification.confidence_score:.0f}%."
            ),
        })

    return qa


# ── Helper functions ──────────────────────────────────────────────────────────

def _pe_interpretation(pe):
    if pe is None:
        return ""
    if pe < 10:
        return "This is below the market average, potentially indicating undervaluation or low growth expectations."
    elif pe < 20:
        return "This is in the moderate range, suggesting fair valuation."
    elif pe < 35:
        return "This is above average, reflecting market premium for quality or growth."
    else:
        return "This is high, typically seen in high-growth or speculative stocks."


def _roe_interpretation(roe):
    if roe is None:
        return ""
    if roe > 25:
        return "indicating exceptional capital efficiency."
    elif roe > 15:
        return "indicating good capital efficiency."
    elif roe > 10:
        return "indicating moderate returns."
    else:
        return "indicating below-average capital efficiency."


def _dividend_answer(company):
    dy = company.dividend_yield
    if dy and dy > 0:
        return (
            f"Yes, {company.name} pays dividends with a current yield of {_fmt_pct(dy)}. "
            + ("This is an attractive yield for income investors." if dy > 2 else
               "The yield is modest but reflects consistent shareholder returns.")
        )
    return (
        f"{company.name} does not currently pay a meaningful dividend. "
        "The company likely reinvests earnings for growth."
    )


def _debt_answer(company, quality):
    de = quality.debt_to_equity
    ic = quality.interest_coverage
    if de is None:
        return "Debt data not available."
    parts = [f"{company.name} has a debt-to-equity ratio of {de:.2f}x."]
    if de < 0.3:
        parts.append("The company carries minimal debt, indicating a very strong balance sheet.")
    elif de < 1:
        parts.append("Debt levels are manageable.")
    elif de < 2:
        parts.append("The company carries moderate leverage, which warrants monitoring.")
    else:
        parts.append("High leverage is a risk factor, especially in a rising interest rate environment.")
    if ic:
        parts.append(f"Interest coverage ratio is {ic:.1f}x.")
    return " ".join(parts)


def _recession_behavior(company, quality):
    sector = (company.sector or "").lower()
    cyclical_keywords = {"steel", "metal", "power", "auto", "oil", "gas", "chemicals"}
    is_cyclical = any(kw in sector for kw in cyclical_keywords)

    if is_cyclical:
        return (
            f"{company.name} operates in a cyclical sector. During recessions, "
            "revenue and profits typically contract with falling commodity prices and demand. "
            "Recovery follows economic revival and improved capacity utilization."
        )
    elif quality.roe and quality.roe > 15 and (quality.debt_to_equity or 1) < 0.5:
        return (
            f"{company.name} has strong profitability and low debt, suggesting relative "
            "resilience during economic downturns. Companies with these characteristics "
            "typically maintain operations and may even gain market share in difficult periods."
        )
    else:
        return (
            f"As a {company.sector} company, {company.name}'s recession performance "
            "would depend on client spending patterns and contract continuity. "
            "Historical data and management commentary would provide better clarity."
        )


def _growth_consistency(growth):
    s1 = growth.sales_growth_1y
    s3 = growth.sales_growth_3y
    s5 = growth.sales_growth_5y

    if all(v and v > 5 for v in [s1, s3, s5]):
        return (
            f"The company has maintained consistent revenue growth across 1Y ({_fmt_pct(s1)}), "
            f"3Y ({_fmt_pct(s3)}), and 5Y ({_fmt_pct(s5)}) periods, reflecting durable business momentum."
        )
    elif s5 and s5 > 5:
        return (
            f"Revenue growth has been positive over 5 years ({_fmt_pct(s5)} CAGR), "
            "though recent growth may have moderated."
        )
    else:
        return "Growth has been uneven across the observed periods; refer to individual year data for deeper analysis."


def _vs_gdp(growth):
    india_gdp_growth = 6.5  # approximate FY25 GDP growth estimate
    s5 = growth.sales_growth_5y
    if s5 is None:
        return f"India's GDP has grown at approximately {india_gdp_growth}% in recent years. Revenue growth data not available for comparison."

    if s5 > india_gdp_growth * 2:
        label = f"significantly faster than GDP ({s5:.1f}% vs ~{india_gdp_growth}%)"
    elif s5 > india_gdp_growth:
        label = f"faster than GDP ({s5:.1f}% vs ~{india_gdp_growth}%)"
    elif s5 > 0:
        label = f"slower than GDP ({s5:.1f}% vs ~{india_gdp_growth}%)"
    else:
        label = f"declining while GDP grew ~{india_gdp_growth}%"

    return (
        f"The company's 5-year revenue CAGR of {_fmt_pct(s5)} is {label}. "
        "India's nominal GDP growth provides a useful baseline for evaluating business performance."
    )
