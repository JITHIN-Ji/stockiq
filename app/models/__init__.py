"""
StockIQ Database Models
All ORM models for the platform
"""

from datetime import datetime
from app import db


class Company(db.Model):
    """Core company information and key metrics."""

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.Float)          # in crores
    current_price = db.Column(db.Float)
    pe_ratio = db.Column(db.Float)
    pb_ratio = db.Column(db.Float)
    dividend_yield = db.Column(db.Float)      # percentage
    listing_year = db.Column(db.Integer)
    face_value = db.Column(db.Float)
    week_high_52 = db.Column(db.Float)
    week_low_52 = db.Column(db.Float)
    book_value = db.Column(db.Float)
    eps = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    growth_metrics = db.relationship("GrowthMetrics", backref="company", uselist=False, cascade="all, delete-orphan")
    quality_metrics = db.relationship("QualityMetrics", backref="company", uselist=False, cascade="all, delete-orphan")
    shareholding = db.relationship("Shareholding", backref="company", uselist=False, cascade="all, delete-orphan")
    classification = db.relationship("Classification", backref="company", uselist=False, cascade="all, delete-orphan")
    insights = db.relationship("Insights", backref="company", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "name": self.name,
            "sector": self.sector,
            "industry": self.industry,
            "market_cap": self.market_cap,
            "current_price": self.current_price,
            "pe_ratio": self.pe_ratio,
            "pb_ratio": self.pb_ratio,
            "dividend_yield": self.dividend_yield,
            "listing_year": self.listing_year,
            "face_value": self.face_value,
            "week_high_52": self.week_high_52,
            "week_low_52": self.week_low_52,
            "book_value": self.book_value,
            "eps": self.eps,
        }

    def __repr__(self):
        return f"<Company {self.ticker}: {self.name}>"


class GrowthMetrics(db.Model):
    """Revenue and profit growth metrics over multiple timeframes."""

    __tablename__ = "growth_metrics"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)

    sales_growth_1y = db.Column(db.Float)
    sales_growth_3y = db.Column(db.Float)
    sales_growth_5y = db.Column(db.Float)

    profit_growth_1y = db.Column(db.Float)
    profit_growth_3y = db.Column(db.Float)
    profit_growth_5y = db.Column(db.Float)

    revenue_ttm = db.Column(db.Float)         # trailing twelve months, in crores
    net_profit_ttm = db.Column(db.Float)

    def to_dict(self):
        return {
            "sales_growth_1y": self.sales_growth_1y,
            "sales_growth_3y": self.sales_growth_3y,
            "sales_growth_5y": self.sales_growth_5y,
            "profit_growth_1y": self.profit_growth_1y,
            "profit_growth_3y": self.profit_growth_3y,
            "profit_growth_5y": self.profit_growth_5y,
            "revenue_ttm": self.revenue_ttm,
            "net_profit_ttm": self.net_profit_ttm,
        }


class QualityMetrics(db.Model):
    """Profitability and balance sheet quality metrics."""

    __tablename__ = "quality_metrics"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)

    roe = db.Column(db.Float)                 # Return on Equity %
    roce = db.Column(db.Float)                # Return on Capital Employed %
    roa = db.Column(db.Float)                 # Return on Assets %
    debt_to_equity = db.Column(db.Float)
    interest_coverage = db.Column(db.Float)
    current_ratio = db.Column(db.Float)
    cash_flow = db.Column(db.Float)           # Operating Cash Flow, crores
    profit_margin = db.Column(db.Float)       # Net profit margin %
    asset_turnover = db.Column(db.Float)

    def to_dict(self):
        return {
            "roe": self.roe,
            "roce": self.roce,
            "roa": self.roa,
            "debt_to_equity": self.debt_to_equity,
            "interest_coverage": self.interest_coverage,
            "current_ratio": self.current_ratio,
            "cash_flow": self.cash_flow,
            "profit_margin": self.profit_margin,
            "asset_turnover": self.asset_turnover,
        }


class Shareholding(db.Model):
    """Shareholder distribution data."""

    __tablename__ = "shareholding"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)

    promoter_holding = db.Column(db.Float)    # %
    fii_holding = db.Column(db.Float)         # %
    dii_holding = db.Column(db.Float)         # %
    public_holding = db.Column(db.Float)      # %
    as_of_date = db.Column(db.String(20))     # e.g. "Sep 2024"

    def to_dict(self):
        return {
            "promoter_holding": self.promoter_holding,
            "fii_holding": self.fii_holding,
            "dii_holding": self.dii_holding,
            "public_holding": self.public_holding,
            "as_of_date": self.as_of_date,
        }


class Classification(db.Model):
    """AI-generated stock classification into Lynch buckets."""

    __tablename__ = "classifications"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)

    primary_bucket = db.Column(db.String(50))    # e.g. "Stalwart", "Fast Grower"
    confidence_score = db.Column(db.Float)        # 0-100
    reasoning_json = db.Column(db.Text)           # JSON list of reasoning points
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        reasoning = []
        if self.reasoning_json:
            try:
                reasoning = json.loads(self.reasoning_json)
            except Exception:
                reasoning = [self.reasoning_json]
        return {
            "primary_bucket": self.primary_bucket,
            "confidence_score": self.confidence_score,
            "reasoning": reasoning,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
        }


class Insights(db.Model):
    """Pre-generated AI narrative insights for each company."""

    __tablename__ = "insights"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), unique=True, nullable=False)

    about_company = db.Column(db.Text)
    future_scope = db.Column(db.Text)
    risks = db.Column(db.Text)
    investment_thesis = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "about_company": self.about_company,
            "future_scope": self.future_scope,
            "risks": self.risks,
            "investment_thesis": self.investment_thesis,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
