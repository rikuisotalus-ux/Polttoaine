import requests
import csv
from datetime import datetime

def scrape_fuels():

    today = datetime.utcnow().strftime("%Y-%m-%d")

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

    rows = []

    for name, symbol in SYMBOLS.items():
        print(f"🔎 Hakee {name}")

        try:
            url = f"https://stooq.com/q/d/l/?s={symbol}&i=d"
            r = requests.get(url, headers=headers, timeout=10)

            # Tarkista että saatiin oikea CSV
            if "Date,Open,High,Low,Close,Volume" not in r.text:
                print(f"⚠️ {name} blocked or invalid data")
                rows.append([name, symbol, None, today])
                continue

            lines = r.text.strip().split("\n")

            if len(lines) >= 2:
                last_line = lines[-1]
                data = last_line.split(",")

                if len(data) >= 5:
                    close_price = data[4]
                else:
                    close_price = None
            else:
                close_price = None

            rows.append([name, symbol, close_price, today])

        except Exception as e:
            print(f"⚠️ {name} fail: {e}")
            rows.append([name, symbol, None, today])

    # ✅ Tallenna CSV
    with open("latest_fuel.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "symbol", "price", "date"])
        writer.writerows(rows)

    print("✅ Tallennettu latest_fuel.csv")


if __name__ == "__main__":
    scrape_fuels()
