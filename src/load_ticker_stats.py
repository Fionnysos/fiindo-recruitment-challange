import requests
from datetime import datetime
from .database import SessionLocal
from .models import Symbol, TickerStatistic

BASE = "https://api.test.fiindo.com/api/v1"
TOKEN = "fionn.zak"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# industries we care about
TARGET_INDUSTRIES = [
    "Banks - Diversified",
    "Software - Application",
    "Consumer Electronics"
]


def fetch_general(symbol):
    # get general info (price etc)
    url = f"{BASE}/general/{symbol}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["fundamentals"]["profile"]["data"][0]


def fetch_income(symbol):
    # income statement data
    url = f"{BASE}/financials/{symbol}/income_statement"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["fundamentals"]["financials"]["income_statement"]["data"]


def fetch_balance(symbol):
    # balance sheet data
    url = f"{BASE}/financials/{symbol}/balance_sheet_statement"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["fundamentals"]["financials"]["balance_sheet_statement"]["data"]


def calc_revenue_growth(last, prev):
    # simple qoq revenue growth
    if not last or not prev or prev == 0:
        return None
    return (last - prev) / prev


def calc_debt_ratio(debt, equity):
    # avoid division issues
    if not equity or equity == 0:
        return None
    if debt is None:
        return None
    return debt / equity


def calc_ttm(values):
    # ttm needs 4 values
    values = [v for v in values if v is not None]
    return sum(values) if len(values) == 4 else None


def build_stats(symbol_obj):
    # build all metrics for one ticker
    symbol = symbol_obj.symbol

    income = sorted(fetch_income(symbol), key=lambda x: x.get("date", ""), reverse=True)
    last = income[0]
    prev = income[1] if len(income) > 1 else None

    rev_last = last.get("revenue")
    rev_prev = prev.get("revenue") if prev else None
    revenue_growth = calc_revenue_growth(rev_last, rev_prev)

    ttm_netincome = calc_ttm([row.get("netIncome") for row in income[:4]])

    balance = sorted(fetch_balance(symbol), key=lambda x: x.get("date", ""), reverse=True)
    bal_last = balance[0]
    debt = bal_last.get("totalDebt")
    equity = bal_last.get("totalStockholdersEquity")
    debt_ratio = calc_debt_ratio(debt, equity)

    profile = fetch_general(symbol)
    price = profile.get("price")

    # eps fallback
    eps = (
        last.get("eps")
        or last.get("epsdiluted")
        or (
            (last.get("netIncome") / last.get("weightedAverageShsOut"))
            if last.get("netIncome") and last.get("weightedAverageShsOut")
            else None
        )
    )

    if price not in (None, 0) and eps not in (None, 0):
        pe_ratio = price / eps
    else:
        pe_ratio = None

    return dict(
        pe_ratio=pe_ratio,
        revenue_growth=revenue_growth,
        net_income_ttm=ttm_netincome,
        debt_ratio=debt_ratio,
        revenue_last_quarter=rev_last,
        calculated_at=datetime.utcnow().isoformat()
    )


def save_stats(session, symbol_obj, stats):
    # clear old stats and insert new ones
    session.query(TickerStatistic).filter_by(symbol_id=symbol_obj.id).delete()
    session.add(TickerStatistic(symbol_id=symbol_obj.id, **stats))


from sqlalchemy import or_


def main():
    # load all symbols we need
    session = SessionLocal()

    symbols = (
        session.query(Symbol)
        .filter(
            or_(
                Symbol.industry.in_([
                    "Banks - Diversified",
                    "Software - Application"
                ]),
                Symbol.sector == "Consumer Cyclical"  # fallback for electronics
            )
        )
        .all()
    )

    print(f"{len(symbols)} symbols found")

    for i, sym in enumerate(symbols, start=1):
        print(f"[{i}/{len(symbols)}] {sym.symbol}")
        try:
            stats = build_stats(sym)
            save_stats(session, sym, stats)
        except Exception as e:
            print(f"error for {sym.symbol}: {e}")
            continue

    session.commit()
    session.close()
    print("done")


if __name__ == "__main__":
    main()
