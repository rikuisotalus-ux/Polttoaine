import requests
import csv
from datetime import datetime

def scrape_fuels():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    rows = []

    SYMBOLS = {
        "WTI_OIL": "cl.f",
        "BRENT_OIL": "cb.f",
        "NATGAS": "tg.f",
        "CO2": "ev.f",
        "COAL": "lu.f"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/csv"
    }

    for name, symbol in SYMBOLS.items():

        print(f"🔎 Hakee {name} (Stooq LAST)")

        try:
            params = {
                "s": symbol,
                "f": "sd2t2ohlcv",
                "h": "",
                "e": "csv"
            }

            r = requests.get(
                "https://stooq.com/q/l/",
                params=params,
                headers=headers
            )

            last_price = None

            lines = [l for l in r.text.splitlines() if l.strip()]

            if len(lines) >= 2:
                data = lines[1].split(",")

                if len(data) > 6:
                    val = data[6]
                    last_price = None if val in ["", "N/D"] else val

            rows.append([
                name,
                symbol,
                last_price,
                today
            ])

        except Exception as e:
            print(f"⚠️ {name} fail: {e}")

    return rows


if __name__ == "__main__":
    data = scrape_fuels()
    print(data)
