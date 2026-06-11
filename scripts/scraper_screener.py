

import re
import time
import requests
import yfinance as yf
from bs4 import BeautifulSoup



TICKERS = [
    "TCS", "INFY", "WIPRO", "PERSISTENT",
    "SAIL", "ADANIPOWER", "ONGC", "VEDL",
    "YESBANK", "RELIANCE",
]

# NSE suffix for yfinance
YF_SUFFIX = ".NS"

# Screener.in slug (some tickers differ from NSE symbol)
SCREENER_SLUG = {
    "TCS":        "TCS",
    "INFY":       "INFY",
    "WIPRO":      "WIPRO",
    "PERSISTENT": "PERSISTENT",
    "SAIL":       "SAIL",
    "ADANIPOWER": "ADANI-POWER",
    "ONGC":       "ONGC",
    "VEDL":       "VEDL",
    "YESBANK":    "YESBANK",
    "RELIANCE":   "RELIANCE",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.screener.in/",
}




def _parse_num(text: str):
    if not text:
        return None
    cleaned = str(text).replace(",", "").replace("%", "").strip()
    if " - " in cleaned:
        cleaned = cleaned.split(" - ")[0].strip()
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def _to_crore(value) -> float | None:
    """Convert raw INR value (from yfinance) to crores."""
    if value is None:
        return None
    try:
        return round(float(value) / 1e7, 2)
    except (ValueError, TypeError):
        return None


def _cagr(start, end, years) -> float | None:
    """Calculate CAGR % between two values over N years."""
    if not start or not end or years <= 0:
        return None
    if start <= 0:
        return None
    try:
        return round(((end / start) ** (1 / years) - 1) * 100, 2)
    except Exception:
        return None



def _yf_data(ticker: str) -> dict:
    """
    Pull all available data from yfinance for a NSE ticker.
    Returns merged dict for company + growth + quality sections.
    """
    t = yf.Ticker(ticker + YF_SUFFIX)
    info = t.info or {}

    # ── Company basics ─────────────────────────────────────────────────────────
    market_cap    = _to_crore(info.get("marketCap"))
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    pe_ratio      = info.get("trailingPE") or info.get("forwardPE")
    pb_ratio      = info.get("priceToBook")
    div_yield     = info.get("dividendYield")
    if div_yield:
        div_yield = round(div_yield * 100, 2)   # convert 0.016 → 1.6%
    week_high     = info.get("fiftyTwoWeekHigh")
    week_low      = info.get("fiftyTwoWeekLow")
    book_value    = info.get("bookValue")
    eps           = info.get("trailingEps")
    sector        = info.get("sector")
    industry      = info.get("industry")
    name          = info.get("longName") or info.get("shortName")

    # Listing year from firstTradeDateEpochUtc
    listing_year = None
    ipo = info.get("firstTradeDateEpochUtc")
    if ipo:
        from datetime import datetime
        listing_year = datetime.utcfromtimestamp(ipo).year

    # Face value — yfinance doesn't have it; will get from Screener
    face_value = None

    
    try:
        fin = t.financials          # annual, columns = dates descending
        # Rows we need
        rev_row    = None
        profit_row = None

        for row_name in fin.index:
            rl = row_name.lower()
            if "total revenue" in rl or "operating revenue" in rl:
                rev_row = fin.loc[row_name]
            if "net income" in rl and "minority" not in rl and "discontinued" not in rl:
                if profit_row is None:
                    profit_row = fin.loc[row_name]

        # Columns are datetime index, sort ascending (oldest first)
        def _sorted_vals(row):
            if row is None:
                return []
            s = row.dropna().sort_index()
            return [float(v) for v in s.values]
        rev_vals    = _sorted_vals(rev_row)
        profit_vals = _sorted_vals(profit_row)

        # Revenue TTM = latest value in crores
        revenue_ttm    = _to_crore(rev_vals[-1])    if rev_vals    else None
        net_profit_ttm = _to_crore(profit_vals[-1]) if profit_vals else None

        
        def _growth(vals, years):
            if len(vals) > years:
                return _cagr(vals[-(years+1)], vals[-1], years)
            return None

        sales_1y = _growth(rev_vals, 1)
        sales_3y = _growth(rev_vals, 3)
        sales_5y = _growth(rev_vals, 4) or sales_3y   # 4Y max, fallback 3Y

        profit_1y = _growth(profit_vals, 1)
        profit_3y = _growth(profit_vals, 3)
        profit_5y = _growth(profit_vals, 4) or profit_3y

    except Exception as e:
        print(f"    [yf financials warn] {e}")
        revenue_ttm = net_profit_ttm = None
        sales_1y = sales_3y = sales_5y = None
        profit_1y = profit_3y = profit_5y = None

    
   
    profit_margin = info.get("profitMargins")
    if profit_margin:
        profit_margin = round(profit_margin * 100, 2)

    roe = info.get("returnOnEquity")
    if roe:
        roe = round(roe * 100, 2)

    roa = info.get("returnOnAssets")
    if roa:
        roa = round(roa * 100, 2)

    debt_to_equity = info.get("debtToEquity")
    if debt_to_equity:
        debt_to_equity = round(debt_to_equity / 100, 2)

    current_ratio = info.get("currentRatio")

    # Cash flow from operations (TTM)
    cash_flow = None
    try:
        cf = t.cashflow
        for row_name in cf.index:
            if "operating" in row_name.lower():
                vals = cf.loc[row_name].dropna()
                if not vals.empty:
                    cash_flow = _to_crore(vals.iloc[0])
                    break
    except Exception:
        pass

    # Asset turnover = Revenue / Total Assets (latest year)
    asset_turnover = None
    try:
        bs = t.balance_sheet
        total_assets_row = None
        for row_name in bs.index:
            if "total assets" in row_name.lower():
                total_assets_row = bs.loc[row_name]
                break
        if total_assets_row is not None and rev_vals:
            assets = total_assets_row.dropna().iloc[0]
            if assets and assets > 0:
                asset_turnover = round(float(rev_vals[-1]) / float(assets), 2)
    except Exception:
        pass

    return {
        "company": {
            "name":          name,
            "sector":        sector,
            "industry":      industry,
            "market_cap":    market_cap,
            "current_price": current_price,
            "pe_ratio":      pe_ratio,
            "pb_ratio":      pb_ratio,
            "dividend_yield": div_yield,
            "listing_year":  listing_year,
            "face_value":    face_value,       # filled by Screener
            "week_high_52":  week_high,
            "week_low_52":   week_low,
            "book_value":    book_value,
            "eps":           eps,
        },
        "growth": {
            "sales_growth_1y":  sales_1y,
            "sales_growth_3y":  sales_3y,
            "sales_growth_5y": sales_5y,
            "profit_growth_1y": profit_1y,
            "profit_growth_3y": profit_3y,
            "profit_growth_5y": profit_5y,
            "revenue_ttm":      revenue_ttm,
            "net_profit_ttm":   net_profit_ttm,
        },
        "quality": {
            "roe":               roe,
            "roce":              None,   # Screener
            "roa":               roa,
            "debt_to_equity":    debt_to_equity,
            "interest_coverage": None,   # updated in screener data
            "current_ratio":     current_ratio,
            "cash_flow":         cash_flow,
            "profit_margin":     profit_margin,
            "asset_turnover":    asset_turnover,
        },
    }




def _get_screener_soup(ticker: str) -> BeautifulSoup | None:
    slug = SCREENER_SLUG.get(ticker, ticker)
    for variant in ["consolidated", ""]:
        suffix = f"/{variant}/" if variant else "/"
        url = f"https://www.screener.in/company/{slug}{suffix}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            if r.status_code == 200:
                return BeautifulSoup(r.text, "html.parser")
        except Exception as e:
            print(f"    [screener warn] {e}")
    return None


def _screener_ratio(soup: BeautifulSoup, label: str):
    """Get a value from #top-ratios by label name."""
    section = soup.find(id="top-ratios")
    if not section:
        return None
    for li in section.find_all("li"):
        name_span = li.find("span", class_="name")
        val_span  = li.find("span", class_="nowrap") or li.find("span", class_="value")
        if name_span and val_span:
            if label.lower() in name_span.get_text(strip=True).lower():
                return _parse_num(val_span.get_text(strip=True))
    return None


def _screener_shareholding(soup: BeautifulSoup) -> dict:
    result = {
        "promoter_holding": None,
        "fii_holding":      None,
        "dii_holding":      None,
        "public_holding":   None,
        "as_of_date":       None,
    }
    section = soup.find(id="shareholding")
    if not section:
        return result

    quarterly = section.find(id="quarterly-shp")
    table = (quarterly or section).find("table")
    if not table:
        return result

    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    quarters = [h for h in headers if h and "shareholding" not in h.lower()]
    if quarters:
        result["as_of_date"] = quarters[-1]

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells or len(cells) < 2:
            continue
        label = cells[0].get_text(strip=True).lower()
        val   = _parse_num(cells[-1].get_text(strip=True))
        if "promoter" in label:
            result["promoter_holding"] = val
        elif "fii" in label or "foreign" in label:
            result["fii_holding"] = val
        elif "dii" in label or "domestic" in label:
            result["dii_holding"] = val
        elif "public" in label:
            result["public_holding"] = val

    return result


def _screener_data(ticker: str) -> dict:
    """
    Pull ratios + shareholding from Screener.in HTML.
    Only #top-ratios and #shareholding sections — both confirmed working.
    """
    soup = _get_screener_soup(ticker)
    if not soup:
        return {"ratios": {}, "shareholding": {}}

    ratios = {
        "face_value":        _screener_ratio(soup, "Face Value"),
        "roce":              _screener_ratio(soup, "ROCE"),
        "interest_coverage": _screener_ratio(soup, "Interest Coverage"),
    }
    shareholding = _screener_shareholding(soup)
    return {"ratios": ratios, "shareholding": shareholding}



def scrape_ticker(ticker: str) -> dict | None:
    """
    Scrape one ticker using both yfinance + Screener.
    Returns dict ready for DB insert.
    """
    print(f"  {ticker}...", end=" ", flush=True)

    try:
        yf_result = _yf_data(ticker)
    except Exception as e:
        print(f"FAILED yfinance: {e}")
        return None

    try:
        sc_result = _screener_data(ticker)
    except Exception as e:
        print(f"[screener partial fail: {e}]", end=" ")
        sc_result = {"ratios": {}, "shareholding": {}}

    # Merge: yfinance base + Screener fills gaps
    ratios = sc_result["ratios"]

    yf_result["company"]["face_value"] = ratios.get("face_value")
    yf_result["quality"]["roce"]              = ratios.get("roce")
    yf_result["quality"]["interest_coverage"] = ratios.get("interest_coverage")

    yf_result["company"]["ticker"] = ticker
    yf_result["shareholding"]      = sc_result["shareholding"]

    print("OK")
    return yf_result


def scrape_all() -> list[dict]:
    """Scrape all tickers. 2s delay between each."""
    results = []
    for ticker in TICKERS:
        data = scrape_ticker(ticker)
        if data:
            results.append(data)
        time.sleep(2)
    return results