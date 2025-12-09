import requests
from .database import SessionLocal
from .models import Symbol

BASE = "https://api.test.fiindo.com"
TOKEN = "fionn.zak"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def fetch_symbols():
    # get list of all symbols
    resp = requests.get(f"{BASE}/api/v1/symbols", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["symbols"]


def fetch_profile(symbol_code: str) -> dict:
    # get company profile
    resp = requests.get(f"{BASE}/api/v1/general/{symbol_code}", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data["fundamentals"]["profile"]["data"][0]


def save_symbol(session, symbol_code: str, profile: dict):
    # check if symbol exists
    existing = session.query(Symbol).filter_by(symbol=symbol_code).first()

    if existing is None:
        # create new DB entry
        sym = Symbol(
            symbol=symbol_code,
            code=profile.get("symbol"),
            exchange=profile.get("exchangeShortName"),
            company_name=profile.get("companyName"),
            sector=profile.get("sector"),
            industry=profile.get("industry"),
            country=profile.get("country"),
            currency=profile.get("currency"),
            market_cap=profile.get("mktCap"),
        )
        session.add(sym)
    else:
        # update existing entry
        existing.company_name = profile.get("companyName")
        existing.sector = profile.get("sector")
        existing.industry = profile.get("industry")
        existing.market_cap = profile.get("mktCap")


def main():
    session = SessionLocal()
    try:
        # load all symbols
        symbols = fetch_symbols()
        print(f"{len(symbols)} symbols found")

        # continue at 385
        for i, symbol_code in enumerate(symbols, start=1):
            if i > len(symbols):
                break

            print(f"[{i}/{len(symbols)}] handling {symbol_code}")
            profile = fetch_profile(symbol_code)
            save_symbol(session, symbol_code, profile)

        session.commit()
        print("done")
    finally:
        session.close()


if __name__ == "__main__":
    main()
