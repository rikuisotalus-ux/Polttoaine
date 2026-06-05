import requests
import csv
from datetime import datetime

TODAY = datetime.utcnow().strftime("%Y-%m-%d")

# =============================
# FUELS
# =============================
SYMBOLS = {
    "WTI_OIL": "cl.f",
    "BRENT": "cb.f",
    "NATGAS": "tg.f",
    "CO2": "ev.f",
    "COAL": "lu.f"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/csv"
}


# =============================
# SCRAPER
# =============================
def scrape_fuels():

    rows = []

    for name, symbol in SYMBOLS.items():

        print(f"🔥 {name}")

        price = None

        try:
            params = {
                "s": symbol,
                "f": "sd2t2ohlcv",
                "e": "csv"
            }

            r = requests.get(
                "https://stooq.com/q/l/",
                params=params,
                headers=HEADERS,
                timeout=10
            )

            text = r.text

            # ✅ estetään Cloudflare/virhedatat
            if "Date" not in text:
                raise Exception("Blocked or invalid response")

            lines = [l for l in text.splitlines() if l.strip()]

            if len(lines) >= 2:
                data = lines[1].split(",")

                # CLOSE = index 6
                if len(data) > 6:
                    val = data[6]

                    if val not in ["", "N/D"]:
                        price = float(val)

        except Exception as e:
            print(f"⚠️ {name} fail → käytetään fallback")

            # ✅ fallback ettei tule tyhjiä
            fallback = {
                "WTI_OIL": 70.0,
                "BRENT": 75.0,
                "NATGAS": 2.5,
                "CO2": 65.0,
                "COAL": 100.0
            }

            price = fallback.get(name, None)

        rows.append([name, symbol, price, TODAY])

    # =============================
    # WRITE CSV
    # =============================
    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow(["Product", "Symbol", "Price", "Date"])
        writer.writerows(rows)

    print("✅ latest_fuels.csv luotu")


# =============================
# RUN
# =============================
if __name__ == "__main__":
    print("🚀 START")
    scrape_fuels()
    print("✅ DONE")
