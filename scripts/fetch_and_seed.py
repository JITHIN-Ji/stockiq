

import os


def save_company(db, data: dict) -> int | None:
    """
    Insert one company + related metrics into DB.
    Returns company.id on success, None on failure.
    """
    from app.models import Company, GrowthMetrics, QualityMetrics, Shareholding

    try:
        # Company
        company = Company(**data["company"])
        db.session.add(company)
        db.session.flush()  # get company.id

        # Growth
        if data.get("growth"):
            db.session.add(GrowthMetrics(company_id=company.id, **data["growth"]))

        # Quality
        if data.get("quality"):
            db.session.add(QualityMetrics(company_id=company.id, **data["quality"]))

        # Shareholding
        if data.get("shareholding"):
            db.session.add(Shareholding(company_id=company.id, **data["shareholding"]))

        db.session.commit()
        return company.id

    except Exception as e:
        db.session.rollback()
        print(f"    ❌ DB save failed: {e}")
        return None


def fetch_and_seed():
    """
    Full pipeline:
    clear → scrape → save
    Classifications and insights are run via admin panel.
    Called from run.py on startup when DB is empty.
    """
    from app import db
    from scripts.scraper_screener import scrape_all

    # Step 1: Scrape
    print("🌐 Scraping Screener.in for all tickers...")
    scraped = scrape_all()
    print(f"   Scraped {len(scraped)} companies.\n")

    if not scraped:
        print("❌ No data scraped. Aborting.")
        return

    # Step 2: Save to DB
    print("💾 Saving to Supabase...")
    company_ids = []
    for data in scraped:
        ticker = data["company"]["ticker"]
        cid = save_company(db, data)
        if cid:
            company_ids.append((ticker, cid))
            print(f"   ✅ {ticker} saved (id={cid})")
        else:
            print(f"   ❌ {ticker} failed to save")

    print(f"\n   Saved {len(company_ids)}/{len(scraped)} companies.\n")

    print("\n💡 Note: Run 'Classify' and 'Generate Insights' from the admin panel to process companies.")
    print("🎉 fetch_and_seed complete.")