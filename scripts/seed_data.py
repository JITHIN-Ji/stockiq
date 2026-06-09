"""
StockIQ Seed Data
Manually sourced financial metrics from Screener.in for all 10 MVP stocks.
Data approximate as of FY2024/Q3 2024.
"""

from app import db
from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding

SEED_DATA = [
    {
        "company": {
            "ticker": "TCS",
            "name": "Tata Consultancy Services",
            "sector": "Information Technology",
            "industry": "IT Consulting & Software",
            "market_cap": 1450000,
            "current_price": 3975,
            "pe_ratio": 30.2,
            "pb_ratio": 13.5,
            "dividend_yield": 1.6,
            "listing_year": 2004,
            "face_value": 1,
            "week_high_52": 4592,
            "week_low_52": 3311,
            "book_value": 294,
            "eps": 130,
        },
        "growth": {
            "sales_growth_1y": 8.2,
            "sales_growth_3y": 13.5,
            "sales_growth_5y": 11.8,
            "profit_growth_1y": 9.0,
            "profit_growth_3y": 12.3,
            "profit_growth_5y": 10.5,
            "revenue_ttm": 240893,
            "net_profit_ttm": 46099,
        },
        "quality": {
            "roe": 52.1,
            "roce": 65.4,
            "roa": 28.0,
            "debt_to_equity": 0.07,
            "interest_coverage": 84.0,
            "current_ratio": 2.4,
            "cash_flow": 48000,
            "profit_margin": 19.1,
            "asset_turnover": 1.5,
        },
        "shareholding": {
            "promoter_holding": 72.3,
            "fii_holding": 12.5,
            "dii_holding": 6.8,
            "public_holding": 8.4,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "INFY",
            "name": "Infosys",
            "sector": "Information Technology",
            "industry": "IT Consulting & Software",
            "market_cap": 730000,
            "current_price": 1760,
            "pe_ratio": 26.8,
            "pb_ratio": 7.9,
            "dividend_yield": 2.4,
            "listing_year": 1993,
            "face_value": 5,
            "week_high_52": 1990,
            "week_low_52": 1290,
            "book_value": 222,
            "eps": 65.6,
        },
        "growth": {
            "sales_growth_1y": 4.0,
            "sales_growth_3y": 12.8,
            "sales_growth_5y": 12.2,
            "profit_growth_1y": 7.0,
            "profit_growth_3y": 9.5,
            "profit_growth_5y": 9.8,
            "revenue_ttm": 158000,
            "net_profit_ttm": 26248,
        },
        "quality": {
            "roe": 31.7,
            "roce": 40.5,
            "roa": 19.3,
            "debt_to_equity": 0.16,
            "interest_coverage": 52.0,
            "current_ratio": 2.6,
            "cash_flow": 29000,
            "profit_margin": 16.6,
            "asset_turnover": 1.3,
        },
        "shareholding": {
            "promoter_holding": 14.7,
            "fii_holding": 32.1,
            "dii_holding": 23.5,
            "public_holding": 29.7,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "WIPRO",
            "name": "Wipro",
            "sector": "Information Technology",
            "industry": "IT Consulting & Software",
            "market_cap": 245000,
            "current_price": 468,
            "pe_ratio": 22.4,
            "pb_ratio": 3.8,
            "dividend_yield": 0.2,
            "listing_year": 1945,
            "face_value": 2,
            "week_high_52": 575,
            "week_low_52": 380,
            "book_value": 123,
            "eps": 20.9,
        },
        "growth": {
            "sales_growth_1y": -4.4,
            "sales_growth_3y": 8.5,
            "sales_growth_5y": 10.1,
            "profit_growth_1y": 4.5,
            "profit_growth_3y": 7.0,
            "profit_growth_5y": 8.9,
            "revenue_ttm": 90000,
            "net_profit_ttm": 11100,
        },
        "quality": {
            "roe": 17.1,
            "roce": 22.0,
            "roa": 10.2,
            "debt_to_equity": 0.21,
            "interest_coverage": 24.0,
            "current_ratio": 2.1,
            "cash_flow": 14000,
            "profit_margin": 12.3,
            "asset_turnover": 0.9,
        },
        "shareholding": {
            "promoter_holding": 72.9,
            "fii_holding": 7.8,
            "dii_holding": 6.9,
            "public_holding": 12.4,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "PERSISTENT",
            "name": "Persistent Systems",
            "sector": "Information Technology",
            "industry": "IT Consulting & Software",
            "market_cap": 88000,
            "current_price": 5800,
            "pe_ratio": 64.0,
            "pb_ratio": 17.2,
            "dividend_yield": 0.5,
            "listing_year": 2010,
            "face_value": 10,
            "week_high_52": 6789,
            "week_low_52": 3500,
            "book_value": 337,
            "eps": 90.6,
        },
        "growth": {
            "sales_growth_1y": 18.8,
            "sales_growth_3y": 33.5,
            "sales_growth_5y": 28.7,
            "profit_growth_1y": 35.4,
            "profit_growth_3y": 52.0,
            "profit_growth_5y": 42.0,
            "revenue_ttm": 9600,
            "net_profit_ttm": 1100,
        },
        "quality": {
            "roe": 29.0,
            "roce": 38.0,
            "roa": 18.5,
            "debt_to_equity": 0.01,
            "interest_coverage": 120.0,
            "current_ratio": 2.8,
            "cash_flow": 1200,
            "profit_margin": 11.5,
            "asset_turnover": 1.7,
        },
        "shareholding": {
            "promoter_holding": 31.2,
            "fii_holding": 28.5,
            "dii_holding": 16.3,
            "public_holding": 24.0,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "SAIL",
            "name": "Steel Authority of India",
            "sector": "Metals & Mining",
            "industry": "Steel",
            "market_cap": 41000,
            "current_price": 99,
            "pe_ratio": 11.8,
            "pb_ratio": 0.8,
            "dividend_yield": 2.5,
            "listing_year": 1995,
            "face_value": 10,
            "week_high_52": 175,
            "week_low_52": 82,
            "book_value": 120,
            "eps": 8.4,
        },
        "growth": {
            "sales_growth_1y": -8.5,
            "sales_growth_3y": 5.8,
            "sales_growth_5y": 4.2,
            "profit_growth_1y": -42.0,
            "profit_growth_3y": 8.0,
            "profit_growth_5y": 3.5,
            "revenue_ttm": 98000,
            "net_profit_ttm": 3500,
        },
        "quality": {
            "roe": 6.5,
            "roce": 9.2,
            "roa": 2.8,
            "debt_to_equity": 0.95,
            "interest_coverage": 3.2,
            "current_ratio": 1.2,
            "cash_flow": 5000,
            "profit_margin": 3.5,
            "asset_turnover": 0.7,
        },
        "shareholding": {
            "promoter_holding": 65.0,
            "fii_holding": 5.0,
            "dii_holding": 16.5,
            "public_holding": 13.5,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "ADANIPOWER",
            "name": "Adani Power",
            "sector": "Power",
            "industry": "Thermal Power",
            "market_cap": 195000,
            "current_price": 507,
            "pe_ratio": 10.5,
            "pb_ratio": 3.8,
            "dividend_yield": 0.0,
            "listing_year": 2009,
            "face_value": 10,
            "week_high_52": 900,
            "week_low_52": 430,
            "book_value": 133,
            "eps": 48.3,
        },
        "growth": {
            "sales_growth_1y": 22.0,
            "sales_growth_3y": 35.0,
            "sales_growth_5y": 18.5,
            "profit_growth_1y": 85.0,
            "profit_growth_3y": 120.0,
            "profit_growth_5y": 45.0,
            "revenue_ttm": 55000,
            "net_profit_ttm": 18600,
        },
        "quality": {
            "roe": 34.2,
            "roce": 18.5,
            "roa": 8.9,
            "debt_to_equity": 1.8,
            "interest_coverage": 4.2,
            "current_ratio": 0.9,
            "cash_flow": 12000,
            "profit_margin": 33.8,
            "asset_turnover": 0.4,
        },
        "shareholding": {
            "promoter_holding": 74.9,
            "fii_holding": 3.2,
            "dii_holding": 4.1,
            "public_holding": 17.8,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "ONGC",
            "name": "Oil and Natural Gas Corporation",
            "sector": "Oil & Gas",
            "industry": "Crude Oil & Natural Gas",
            "market_cap": 320000,
            "current_price": 254,
            "pe_ratio": 7.8,
            "pb_ratio": 0.9,
            "dividend_yield": 4.5,
            "listing_year": 1994,
            "face_value": 5,
            "week_high_52": 345,
            "week_low_52": 200,
            "book_value": 282,
            "eps": 32.6,
        },
        "growth": {
            "sales_growth_1y": -5.2,
            "sales_growth_3y": 12.0,
            "sales_growth_5y": 6.5,
            "profit_growth_1y": -15.0,
            "profit_growth_3y": 18.0,
            "profit_growth_5y": 5.0,
            "revenue_ttm": 617000,
            "net_profit_ttm": 40800,
        },
        "quality": {
            "roe": 11.5,
            "roce": 14.8,
            "roa": 5.9,
            "debt_to_equity": 0.52,
            "interest_coverage": 7.5,
            "current_ratio": 1.4,
            "cash_flow": 55000,
            "profit_margin": 6.6,
            "asset_turnover": 0.6,
        },
        "shareholding": {
            "promoter_holding": 58.9,
            "fii_holding": 8.4,
            "dii_holding": 21.2,
            "public_holding": 11.5,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "VEDL",
            "name": "Vedanta",
            "sector": "Metals & Mining",
            "industry": "Diversified Metals",
            "market_cap": 165000,
            "current_price": 445,
            "pe_ratio": 13.5,
            "pb_ratio": 3.2,
            "dividend_yield": 8.5,
            "listing_year": 1995,
            "face_value": 1,
            "week_high_52": 527,
            "week_low_52": 215,
            "book_value": 139,
            "eps": 33.0,
        },
        "growth": {
            "sales_growth_1y": -6.8,
            "sales_growth_3y": 10.2,
            "sales_growth_5y": 7.8,
            "profit_growth_1y": -28.0,
            "profit_growth_3y": 5.5,
            "profit_growth_5y": 4.2,
            "revenue_ttm": 142000,
            "net_profit_ttm": 8700,
        },
        "quality": {
            "roe": 22.8,
            "roce": 15.2,
            "roa": 6.8,
            "debt_to_equity": 1.95,
            "interest_coverage": 2.8,
            "current_ratio": 0.8,
            "cash_flow": 18000,
            "profit_margin": 6.1,
            "asset_turnover": 0.7,
        },
        "shareholding": {
            "promoter_holding": 59.9,
            "fii_holding": 12.5,
            "dii_holding": 11.8,
            "public_holding": 15.8,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "YESBANK",
            "name": "Yes Bank",
            "sector": "Banking & Finance",
            "industry": "Private Sector Bank",
            "market_cap": 38000,
            "current_price": 19.5,
            "pe_ratio": 28.0,
            "pb_ratio": 1.2,
            "dividend_yield": 0.0,
            "listing_year": 2005,
            "face_value": 2,
            "week_high_52": 32,
            "week_low_52": 18,
            "book_value": 16.3,
            "eps": 0.7,
        },
        "growth": {
            "sales_growth_1y": 22.5,
            "sales_growth_3y": 14.0,
            "sales_growth_5y": -8.0,
            "profit_growth_1y": 140.0,
            "profit_growth_3y": None,
            "profit_growth_5y": None,
            "revenue_ttm": 25000,
            "net_profit_ttm": 1400,
        },
        "quality": {
            "roe": 4.2,
            "roce": 5.8,
            "roa": 0.5,
            "debt_to_equity": 9.2,
            "interest_coverage": 1.2,
            "current_ratio": None,
            "cash_flow": 2000,
            "profit_margin": 5.6,
            "asset_turnover": 0.1,
        },
        "shareholding": {
            "promoter_holding": 0.0,
            "fii_holding": 12.8,
            "dii_holding": 23.4,
            "public_holding": 63.8,
            "as_of_date": "Sep 2024",
        },
    },
    {
        "company": {
            "ticker": "RELIANCE",
            "name": "Reliance Industries",
            "sector": "Conglomerate",
            "industry": "Oil Refining & Petrochemicals",
            "market_cap": 1700000,
            "current_price": 2520,
            "pe_ratio": 28.5,
            "pb_ratio": 2.4,
            "dividend_yield": 0.4,
            "listing_year": 1977,
            "face_value": 10,
            "week_high_52": 3218,
            "week_low_52": 2200,
            "book_value": 1050,
            "eps": 88.5,
        },
        "growth": {
            "sales_growth_1y": 2.5,
            "sales_growth_3y": 14.5,
            "sales_growth_5y": 13.2,
            "profit_growth_1y": 6.5,
            "profit_growth_3y": 15.8,
            "profit_growth_5y": 14.0,
            "revenue_ttm": 976000,
            "net_profit_ttm": 69600,
        },
        "quality": {
            "roe": 8.6,
            "roce": 10.9,
            "roa": 4.2,
            "debt_to_equity": 0.44,
            "interest_coverage": 5.8,
            "current_ratio": 1.3,
            "cash_flow": 85000,
            "profit_margin": 7.1,
            "asset_turnover": 0.6,
        },
        "shareholding": {
            "promoter_holding": 50.3,
            "fii_holding": 23.5,
            "dii_holding": 12.4,
            "public_holding": 13.8,
            "as_of_date": "Sep 2024",
        },
    },
]


def seed_company(record: dict) -> bool:
    """
    Insert or update a single company and all related metrics.
    Returns True if created, False if updated.
    """
    cdata = record["company"]
    company = Company.query.filter_by(ticker=cdata["ticker"]).first()
    is_new = company is None

    if not company:
        company = Company(**cdata)
        db.session.add(company)
    else:
        for k, v in cdata.items():
            setattr(company, k, v)

    db.session.flush()   # Get company.id before inserting related rows

    # Growth Metrics
    gdata = record.get("growth")
    if gdata:
        gm = GrowthMetrics.query.filter_by(company_id=company.id).first()
        if not gm:
            gm = GrowthMetrics(company_id=company.id, **gdata)
            db.session.add(gm)
        else:
            for k, v in gdata.items():
                setattr(gm, k, v)

    # Quality Metrics
    qdata = record.get("quality")
    if qdata:
        qm = QualityMetrics.query.filter_by(company_id=company.id).first()
        if not qm:
            qm = QualityMetrics(company_id=company.id, **qdata)
            db.session.add(qm)
        else:
            for k, v in qdata.items():
                setattr(qm, k, v)

    # Shareholding
    sdata = record.get("shareholding")
    if sdata:
        sh = Shareholding.query.filter_by(company_id=company.id).first()
        if not sh:
            sh = Shareholding(company_id=company.id, **sdata)
            db.session.add(sh)
        else:
            for k, v in sdata.items():
                setattr(sh, k, v)

    db.session.commit()
    return is_new


def seed_all():
    """Seed all companies. Run from CLI or setup script."""
    for record in SEED_DATA:
        seed_company(record)
    print(f"✅ Seeded {len(SEED_DATA)} companies.")
