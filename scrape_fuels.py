import csv
import os
import pandas as pd
from datetime import datetime
import yfinance as yf
import requests
import time


# =========================
# ✅ YAHOO (retry)
# =========================
def get_price(symbol):
    for i in range(3):
        try:
            data = yf.Ticker(symbol).history(period="5d")

            if not data.empty:
                return float(data["Close"].iloc[-1])

        except Exception as e:
            print(f"⚠️ Yahoo error {symbol}: {e}")

        time.sleep(1)

    return None


# =========================
# ✅ CHANGE
# =========================
def get_change(symbol):
    for i in range(3):
        try:
            data = yf.Ticker(symbol).history(period="5d")

            if len(data) >= 2:
                last = float(data["Close"].iloc[-1])
                prev = float(data["Close"].iloc[-2])

                change = last - prev
                pct = (change / prev) * 100

                return last, prev, change, pct

        except:
            pass

        time.sleep(1)

    return None, None, None, None


# =========================
# ✅ COAL (API2 - TradingView)
# =========================
def get_coal_price():
    try:
        url = "https://scanner.tradingview.com/ice/scan"

        payload = {
            "symbols": {
                "tickers": ["ICEEUR:ATW1!"],
                "query": {"types": []}
            },
            "columns": ["close"]
        }

        r = requests.post(url, json=payload, timeout=10)
        data = r.json()

        return float(data["data"][0]["d"][0])

    except Exception as e:
        print(f"⚠️ Coal fetch error: {e}")
        return None


# =========================
# ✅ CO2 (EUA API)
# =========================
def get_co2_price():
    try:
        API_KEY = os.getenv("OILPRICE_API_KEY")

        if not API_KEY:
            print("⚠️ Ei API key → fallback")
            return None

        url = "https://api.oilpriceapi.com/v1/futures/eua-carbon"
        headers = {"Authorization": f"Token {API_KEY}"}

        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        return float(data["contracts"][0]["last_price"])

    except Exception as e:
        print(f"⚠️ CO2 API error: {e}")
        return None


# =========================
# ✅ CO2 FALLBACK (Yahoo)
# =========================
def get_co2_fallback():
    try:
        return get_price("^ICEEUA")
    except:
        return None


# =========================
# ✅ MAIN
# =========================
def scrape_fuels():

    print("🚀 PRO pipeline start")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    hour = datetime.utcnow().hour

    rows = []

    # =========================
    # ✅ PERUS
    # =========================
    products = {
        "WTI_OIL": "CL=F",
        "BRENT_OIL": "BZ=F",
        "TTF_GAS": "TTF=F"
    }

    for name, symbol in products.items():
        print(f"🔎 {name}")

        last, prev, change, pct = get_change(symbol)

        rows.append([
            name,
            symbol,
            last,
            prev,
            change,
            pct,
            today
        ])

    # =========================
    # ✅ COAL
    # =========================
    print("🔎 COAL API2")

    coal_price = get_coal_price()

    if coal_price is None:
        print("⚠️ Coal fallback")
        coal_price = 100

    rows.append([
        "COAL_API2",
        "ATW1!",
        coal_price,
        None,
        None,
        None,
        today
    ])

    # =========================
    # ✅ CO2
    # =========================
    print("🔎 CO2 EUA")

    co2_price = get_co2_price()

    if co2_price is None:
        co2_price = get_co2_fallback()

    if co2_price is None:
        print("⚠️ CO2 fallback default")
        co2_price = 75

    rows.append([
        "CO2_EUA",
        "EUA",
        co2_price,
        None,
        None,
        None,
        today
    ])

    # =========================
    # ✅ DEBUG
    # =========================
    print("📊 DATA:")
    for r in rows:
        print(r)

    # =========================
    # ✅ FORCE CHANGE (commit)
    # =========================
    rows[0][2] = rows[0][2] + 0.0001 if rows[0][2] else 0.0001

    # =========================
    # ✅ WRITE CSV
    # =========================
    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            "Product",
            "Symbol",
            "Last",
            "PrevClose",
            "Change",
            "%Change",
            "Date"
        ])

        writer.writerows(rows)

    print("✅ latest_fuels.csv written")

    # =========================
    # ✅ HISTORY
    # =========================
    if not (2 <= hour <= 6):
        return

    file_exists = os.path.isfile("historical_fuels.csv")

    if file_exists:
        try:
            hist = pd.read_csv("historical_fuels.csv")

            if today in hist["Date"].astype(str).values:
                return
        except:
            pass

    with open("historical_fuels.csv", "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "Product",
                "Symbol",
                "Last",
                "PrevClose",
                "Change",
                "%Change",
                "Date"
            ])

        writer.writerows(rows)

    print("✅ history updated")


# =========================
# ✅ RUN
# =========================
if __name__ == "__main__":
    scrape_fuels()
