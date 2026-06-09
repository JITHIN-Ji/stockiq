import os
from app import create_app, db
from app.models import Company, Insights, GrowthMetrics, QualityMetrics, Shareholding
from app.services.insight_generator import generate_insights
from scripts.seed_data import SEED_DATA


def seed_default_companies():
    if Company.query.first():
        return
    print("📦 Seeding default companies...")
    for row in SEED_DATA:
        company_data = row["company"]
        company = Company(**company_data)
        db.session.add(company)
        db.session.flush()

        if row.get("growth"):
            db.session.add(GrowthMetrics(company_id=company.id, **row["growth"]))
        if row.get("quality"):
            db.session.add(QualityMetrics(company_id=company.id, **row["quality"]))
        if row.get("shareholding"):
            db.session.add(Shareholding(company_id=company.id, **row["shareholding"]))

    db.session.commit()
    print("✅ Seeded.")


def generate_missing_insights():
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY not set. Skipping insight generation.")
        return
    missing = Company.query.outerjoin(Insights).filter(Insights.id.is_(None)).all()
    if not missing:
        return
    print(f"🧠 Generating insights for {len(missing)} companies...")
    for company in missing:
        print(f"  {company.ticker}...", end=" ", flush=True)
        ok = generate_insights(company.id)
        print("✅" if ok else "❌")


app = create_app()

# ✅ Runs for both `python run.py` AND gunicorn
with app.app_context():
    db.create_all()
    seed_default_companies()
    generate_missing_insights()

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)