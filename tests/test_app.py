"""
StockIQ Test Suite
Run with: python -m pytest tests/ -v
"""

import pytest
import json
from app import create_app, db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        _db.create_all()
        # Seed data
        from scripts.seed_data import seed_all
        seed_all()
        from app.services.classifier import classify_and_save
        from app.models import Company
        for c in Company.query.all():
            classify_and_save(c.id)
        from scripts.seed_insights import seed_insights
        seed_insights()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ── Home & Navigation ─────────────────────────────────────────────────────────

def test_home_page(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"StockIQ" in r.data


def test_search_redirect_to_stock(client):
    r = client.get("/search?q=TCS")
    assert r.status_code == 302
    assert "/stock/TCS" in r.headers["Location"]


def test_search_no_results(client):
    r = client.get("/search?q=UNKNOWNSTOCK123")
    assert r.status_code == 200


def test_empty_search_redirects_home(client):
    r = client.get("/search?q=")
    assert r.status_code == 302


# ── Stock Detail Pages ────────────────────────────────────────────────────────

@pytest.mark.parametrize("ticker", [
    "TCS", "INFY", "WIPRO", "PERSISTENT", "SAIL",
    "ADANIPOWER", "ONGC", "VEDL", "YESBANK", "RELIANCE"
])
def test_stock_detail_pages(client, ticker):
    r = client.get(f"/stock/{ticker}")
    assert r.status_code == 200


def test_stock_detail_404(client):
    r = client.get("/stock/DOESNOTEXIST")
    assert r.status_code == 404


# ── API Endpoints ─────────────────────────────────────────────────────────────

def test_api_all_stocks(client):
    r = client.get("/api/stocks")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data) == 10


def test_api_single_stock(client):
    r = client.get("/api/stocks/1")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert "company" in data
    assert "growth_metrics" in data
    assert "quality_metrics" in data
    assert "shareholding" in data
    assert "classification" in data
    assert "insights" in data
    assert "qa" in data


def test_api_search(client):
    r = client.get("/api/search?q=tcs")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert len(data) >= 1
    assert data[0]["ticker"] == "TCS"


def test_api_search_empty(client):
    r = client.get("/api/search?q=")
    assert r.status_code == 200
    assert json.loads(r.data) == []


def test_api_stock_404(client):
    r = client.get("/api/stocks/9999")
    assert r.status_code == 404


# ── Classification Engine ─────────────────────────────────────────────────────

def test_classification_results(client):
    r = client.get("/api/stocks/1")
    data = json.loads(r.data)
    clf = data["classification"]
    assert clf["primary_bucket"] in [
        "Slow Mover", "Stalwart", "Fast Grower",
        "Cyclical", "Turnaround", "Asset Play"
    ]
    assert 0 < clf["confidence_score"] <= 100
    assert len(clf["reasoning"]) > 0


def test_persistent_is_fast_grower(app):
    from app.models import Company
    from app.services.classifier import classify_and_save
    with app.app_context():
        c = Company.query.filter_by(ticker="PERSISTENT").first()
        clf = classify_and_save(c.id)
        assert clf.primary_bucket == "Fast Grower"


def test_yesbank_is_turnaround(app):
    from app.models import Company
    from app.services.classifier import classify_and_save
    with app.app_context():
        c = Company.query.filter_by(ticker="YESBANK").first()
        clf = classify_and_save(c.id)
        assert clf.primary_bucket == "Turnaround"


def test_sail_is_cyclical(app):
    from app.models import Company
    from app.services.classifier import classify_and_save
    with app.app_context():
        c = Company.query.filter_by(ticker="SAIL").first()
        clf = classify_and_save(c.id)
        assert clf.primary_bucket == "Cyclical"


# ── Q&A Engine ────────────────────────────────────────────────────────────────

def test_qa_returns_questions(client):
    r = client.get("/api/stocks/1")
    data = json.loads(r.data)
    qa = data["qa"]
    assert len(qa) >= 8


def test_qa_has_required_fields(client):
    r = client.get("/api/stocks/1")
    data = json.loads(r.data)
    for item in data["qa"]:
        assert "question" in item
        assert "answer" in item
        assert "category" in item
        assert len(item["answer"]) > 10


# ── Insights ──────────────────────────────────────────────────────────────────

def test_insights_present(client):
    r = client.get("/api/stocks/1")
    data = json.loads(r.data)
    ins = data["insights"]
    assert ins is not None
    assert len(ins["about_company"]) > 50
    assert len(ins["future_scope"]) > 50
    assert len(ins["risks"]) > 50
    assert len(ins["investment_thesis"]) > 50
