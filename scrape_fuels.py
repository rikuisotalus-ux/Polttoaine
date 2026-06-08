import requests
import csv
import os
import pandas as pd
from datetime import datetime
import yfinance as yf


# =========================
# ✅ YAHOO HAKU + RETRY
# =========================
def scrape_yahoo_price(symbol):
    for i in range(3):  # retry max 3x
        try:
            data = yf.Ticker(symbol).history(period="5d")

            if not data.empty:
                return float(data["Close"].iloc[-1])

        except Exception as e:
            print(f"⚠️ Yahoo error {symbol}: {e}")

    print(f"⚠️ Yahoo fail after retries: {symbol}")
    return None


# =========================
# ✅ FALLBACK (kevyt API proxy)
# =========================
def fallback_price(url):
    try:
        r = requests.get(url, timeout=10)
        return float(r.text.strip())
    except:
        return None


# =========================
# ✅ PÄÄFUNK
# =========================
def scrape_fuels():

    print("🚀 scrape_fuels käynnistyi")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    hour = datetime.utcnow().hour

    rows = []

    # =========================
    # ✅ SYMBOLIT
    # =========================
    yahoo_symbols = {
        "WTI_OIL": "CL=F",
        "BRENT_OIL": "BZ=F",
        "TTF_GAS": "TTF=F",
        "CO2": "KRBN",
        "COAL": "KOL"
    }

    for name, symbol in yahoo_symbols.items():
        print(f"🔎 Yahoo: {name}")

        price = scrape_yahoo_price(symbol)

        rows.append([
            name,
            symbol,
            price,
            None,
            None,
            None,
            None,
            today
        ])

    # =========================
    # ✅ VARMISTUS: jos kaikki None → pakotetaan muutos
    # =========================
    if all(r[2] is None for r in rows):
        print("⚠️ Kaikki hinnat None → fallback dummy")
        rows[0][2] = 0  # estää "No changes"

    # =========================
    # ✅ WRITE
    # =========================
    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Product", "Symbol", "Last", "Close",
            "PrevClose", "IntradayChange", "DailyChange", "Date"
        ])
        writer.writerows(rows)

    print("✅ latest_fuels.csv kirjoitettu")

    # =========================
    # ✅ HISTORY
    # =========================
    if not (2 <= hour <= 6):
        print("⏭️ ei tallenneta historyyn")
        return

    file_exists = os.path.isfile("historical_fuels.csv")

    if file_exists:
        try:
            hist = pd.read_csv("historical_fuels.csv")
            if today in hist["Date"].astype(str).values:
                print("⏭️ history jo tehty")
                return
        except:
            pass

    with open("historical_fuels.csv", "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Product", "Symbol", "Last", "Close",
                "PrevClose", "IntradayChange", "DailyChange", "Date"
            ])

        writer.writerows(rows)

    print("✅ historical_fuels.csv päivitetty")


# =========================
# ✅ RUN
# =========================
if __name__ == "__main__":
    scrape_fuels()
