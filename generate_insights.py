"""
StockIQ Insight Generation Script
Generates AI narratives for all companies using the Anthropic API.
Run AFTER setup.py and AFTER setting ANTHROPIC_API_KEY.

Usage: python generate_insights.py [ticker]
Example: python generate_insights.py TCS
         python generate_insights.py       # generates for all
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Company
from app.services.insight_generator import generate_insights


def main():
    app = create_app()
    with app.app_context():
        ticker = sys.argv[1].upper() if len(sys.argv) > 1 else None

        if ticker:
            company = Company.query.filter_by(ticker=ticker).first()
            if not company:
                print(f"❌ Company '{ticker}' not found.")
                sys.exit(1)
            companies = [company]
        else:
            companies = Company.query.all()

        print(f"🧠 Generating insights for {len(companies)} company/companies...\n")

        for c in companies:
            print(f"  Processing {c.ticker} ({c.name})...", end=" ", flush=True)
            ok = generate_insights(c.id)
            print("✅" if ok else "❌")

        print("\n✅ Done! Insights stored in database.")


if __name__ == "__main__":
    main()
