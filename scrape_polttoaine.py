import requests
import csv
from datetime import datetime
import re
import os
# POLTTOAINETESTI

def scrape_fuels():

    import requests
    import csv
    import os
    from datetime import datetime
    import pandas as pd

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

                # ✅ .f symboleilla CLOSE = index 6
                if len(data) > 6:
                    val = data[6]
                    last_price = None if val in ["", "N/D"] else val

            rows.append([
                name,
                symbol,
                last_price,
                None,
                None,
                None,
                None,
                today
            ])

        except Exception as e:
            print(f"⚠️ {name} fail: {e}")
if __name__ == "__main__":
    scrape_fuels()
