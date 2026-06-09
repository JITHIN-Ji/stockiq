# StockIQ — AI-Powered Stock Intelligence Platform

> Instant investor intelligence for Indian stocks. No waiting. No guesswork.

---

## What is StockIQ?

StockIQ helps retail investors understand any covered stock in under 60 seconds.
Search for a company and instantly see:

- **Company Overview** — what the business does, its position, and key segments
- **Key Financial Metrics** — P/E, P/B, ROE, ROCE, debt, margins, and more
- **Peter Lynch Classification** — which of 6 buckets the stock belongs to, with reasoning
- **AI-Generated Insights** — future scope, risks, and investment thesis (pre-generated, no runtime AI calls)
- **Investor Q&A** — 12+ predefined questions answered from structured data (no AI)
- **Shareholding Pattern** — promoter, FII, DII, and public breakdown

---

## MVP Stock Coverage

| Ticker | Company | Classification |
|--------|---------|---------------|
| TCS | Tata Consultancy Services | Stalwart |
| INFY | Infosys | Stalwart |
| WIPRO | Wipro | Stalwart |
| PERSISTENT | Persistent Systems | Fast Grower |
| SAIL | Steel Authority of India | Cyclical |
| ADANIPOWER | Adani Power | Cyclical |
| ONGC | Oil and Natural Gas Corporation | Cyclical |
| VEDL | Vedanta | Cyclical |
| YESBANK | Yes Bank | Turnaround |
| RELIANCE | Reliance Industries | Stalwart |

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, Flask, SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML, CSS, Bootstrap 5, Vanilla JS |
| AI (optional) | Anthropic Claude API |
| Deploy | Railway / Render |

---

## Project Structure

```
stockiq/
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # SQLAlchemy ORM models
│   │   └── __init__.py       # Company, GrowthMetrics, QualityMetrics, Shareholding,
│   │                         #   Classification, Insights
│   ├── routes/
│   │   ├── main.py           # Frontend page routes
│   │   ├── api.py            # JSON API endpoints
│   │   └── admin.py          # Admin/data management endpoints
│   ├── services/
│   │   ├── classifier.py     # Rule-based Peter Lynch classification engine
│   │   ├── question_engine.py # Maps investor questions to structured data
│   │   └── insight_generator.py # AI narrative generation (Anthropic API)
│   ├── templates/
│   │   ├── base.html         # Layout with nav, footer
│   │   ├── index.html        # Home page with search
│   │   └── stock_detail.html # Full stock analysis page
│   ├── static/
│   │   ├── css/main.css      # Full design system
│   │   └── js/main.js        # Autocomplete, animations
│   └── template_helpers.py   # Jinja2 filters and globals
├── scripts/
│   ├── seed_data.py          # Financial data for all 10 stocks
│   └── seed_insights.py      # Pre-written static insights
├── tests/
│   └── test_app.py           # 27 tests covering all routes, API, and logic
├── setup.py                  # One-command database setup
├── generate_insights.py      # Optional: regenerate insights via Anthropic API
├── run.py                    # Flask dev server entry point
├── Procfile                  # For Railway/Render deployment
├── requirements.txt
└── .env.example
```

---

## Quick Start

### 1. Clone and install dependencies

```bash
git clone <your-repo>
cd stockiq
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY at minimum
# Set DATABASE_URL for PostgreSQL (optional, defaults to SQLite)
```

### 3. Set up the database

```bash
python setup.py
```

This will:
- Create all database tables
- Seed financial data for all 10 stocks
- Run the classification engine
- Insert pre-written static insights

### 4. Start the development server

```bash
flask run
```

Visit **http://localhost:5000**

---

## Optional: AI-Generated Insights

The app ships with pre-written insights for all 10 stocks. To regenerate them
using the Anthropic Claude API:

```bash
# Add to .env:
ANTHROPIC_API_KEY=your-key-here

# Generate for all stocks:
python generate_insights.py

# Generate for a single stock:
python generate_insights.py TCS
```

---

## API Reference

All endpoints return JSON.

### `GET /api/stocks`
Returns all 10 companies with basic info.

### `GET /api/stocks/<id>`
Full data for one company: metrics, classification, insights, Q&A.

### `GET /api/search?q=<query>`
Autocomplete search by name or ticker. Returns up to 10 matches.

### Admin Endpoints (require `X-Admin-Token` header)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/admin/classify` | Re-run classification engine |
| POST | `/admin/generate-insights` | Regenerate AI insights |
| POST | `/admin/seed` | Re-seed financial data |
| GET | `/admin/status` | Check data completeness |

Set `ADMIN_TOKEN` in `.env` (default: `stockiq-admin-secret`).

---

## Classification Logic

Each stock is classified using a rule-based scoring system across 6 Peter Lynch buckets:

| Bucket | Key Signals |
|--------|------------|
| **Slow Mover** | Revenue growth < 4%, mature industry, high dividend yield |
| **Stalwart** | 8–15% revenue CAGR, large cap, strong balance sheet, consistent profits |
| **Fast Grower** | Revenue & profit CAGR > 20%, small-to-mid cap, expanding market |
| **Cyclical** | Steel, power, oil & gas, metals — earnings tied to commodity cycles |
| **Turnaround** | Improving profitability, debt reduction, recovering from distress |
| **Asset Play** | P/B < 1.2x, resource-heavy businesses, trading below intrinsic value |

---

## Running Tests

```bash
python -m pytest tests/ -v
```

27 tests covering:
- All 10 stock detail pages
- All API endpoints
- Classification accuracy (PERSISTENT → Fast Grower, YESBANK → Turnaround, etc.)
- Q&A engine output quality
- Insights completeness

---

## Deployment (Railway)

1. Push to GitHub
2. Connect repo to Railway
3. Set environment variables:
   - `DATABASE_URL` (Railway PostgreSQL)
   - `SECRET_KEY`
   - `ADMIN_TOKEN`
   - `ANTHROPIC_API_KEY` (optional)
4. Add a start command: `python setup.py && gunicorn run:app`

---

## Architecture Decisions

- **No runtime AI calls**: All insights are pre-generated and stored in the DB.
  Page loads are instant — no LLM latency on the user-facing path.

- **No RAG, no PDF processing**: All data comes from structured financial metrics.
  Clean, auditable, and reproducible.

- **Service layer**: Classification, Q&A, and insight generation are decoupled
  services — easy to test, swap, or extend independently.

- **Static insights + AI upgrade path**: Ships with pre-written insights that
  work without any API key. Run `generate_insights.py` to upgrade to AI-generated
  versions when ready.

---

## Adding More Stocks

1. Add a record to `SEED_DATA` in `scripts/seed_data.py`
2. Add pre-written insights to `scripts/seed_insights.py`
3. Run `python setup.py` (safe to re-run — uses upsert logic)
4. Optionally run `python generate_insights.py <TICKER>` for AI narratives

---

## License

MIT
