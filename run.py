import os
from app import create_app, db
from app.models import Company, Insights, BusinessCanvas


def run_pipeline():
    """Clear → scrape → save → classify → insights."""
    from scripts.fetch_and_seed import fetch_and_seed
    fetch_and_seed()


app = create_app()


if os.getenv("ADMIN_TOKEN"):
    print("🔑 Admin token: loaded from environment")
else:
    print("⚠️  Admin token: using default (set ADMIN_TOKEN in .env for production)")

with app.app_context():
    db.create_all()

    if not Company.query.first():
        print("📭 DB empty. Starting scrape pipeline...")
        run_pipeline()
    else:
        print("✅ DB already populated. Skipping scrape.")

    # Generate insights for any company missing them
    if os.getenv("GEMINI_API_KEY"):
        from app.services.insight_generator import generate_insights
        missing = Company.query.outerjoin(Insights).filter(Insights.id.is_(None)).all()
        if missing:
            print(f"🧠 Generating insights for {len(missing)} companies...")
            for company in missing:
                print(f"  {company.ticker}...", end=" ", flush=True)
                ok = generate_insights(company.id)
                print("✅" if ok else "❌")

        from app.services.insight_generator import generate_business_canvas
        missing_canvas = Company.query.outerjoin(BusinessCanvas).filter(BusinessCanvas.id.is_(None)).all()
        if missing_canvas:
            print(f"🧩 Generating business canvas for {len(missing_canvas)} companies...")
            for company in missing_canvas:
                print(f"  {company.ticker}...", end=" ", flush=True)
                ok = generate_business_canvas(company.id)
                print("✅" if ok else "❌")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)