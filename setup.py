"""
StockIQ Setup Script
Run once to initialise the database, seed data, classify stocks, and add insights.
Usage: python setup.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding, Classification, Insights


def main():
    app = create_app()
    with app.app_context():
        print("📦 Creating database tables...")
        db.create_all()
        print("✅ Tables created.\n")

        print("🌱 Seeding company financial data...")
        from scripts.seed_data import seed_all
        seed_all()

        print("\n🤖 Running classification engine...")
        from app.services.classifier import classify_and_save
        for c in Company.query.all():
            clf = classify_and_save(c.id)
            print(f"   {c.ticker:15s} → {clf.primary_bucket} ({clf.confidence_score:.0f}%)")

        print("\n📝 Seeding static insights...")
        from scripts.seed_insights import seed_insights
        seed_insights()

        print("\n✅ Setup complete! Your StockIQ database is ready.\n")
        print("To start the server:")
        print("   flask run\n")
        print("Visit: http://localhost:5000\n")
        print("Optional — Generate AI insights with Anthropic API:")
        print("   1. Add ANTHROPIC_API_KEY to .env")
        print("   2. python generate_insights.py")


if __name__ == "__main__":
    main()
