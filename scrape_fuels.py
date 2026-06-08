import requests
import csv
import os
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import yfinance as yf


def scrape_yahoo_price(symbol):
    try:
        data = yf.Ticker(symbol).history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1])
    except Exception as e:
        print(f"⚠️ Yahoo error {symbol}: {e}")
    return None


def scrape_investing_price(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.9"
        }

        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            print(f"⚠️ Investing HTTP {r.status_code}")
            return None

        soup = BeautifulSoup(r.text, "lxml")

        price = soup.find("span", {"data-test": "instrument-price-last"})

        if price:
            return float(price.text.replace(",", ""))

        print("⚠️ Investing price not found")
        return None

    except Exception as e:
        print(f"⚠️ Investing error: {e}")
        return None


def scrape_fuels():
    print("🚀 scrape_fuels käynnistyi")

    today = datetime.utcnow().strftime("%Y-%m-%d")
    hour = datetime.utcnow().hour

    rows = []

    # =========================
    # ✅ YAHOO DATA
    # =========================
    yahoo_symbols = {
        "WTI_OIL": "CL=F",
        "BRENT_OIL": "BZ=F",
        "TTF_GAS": "TTF=F",
        "CO2_PROXY": "KRBN",
        "COAL_PROXY": "KOL",
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
    # ✅ INVESTING DATA (Oikeat benchmarkit)
    # =========================

    coal_price = scrape_investing_price(
        "https://www.investing.com/commodities/rotterdam-coal-futures"
    )

    rows.append([
        "COAL_API2",
        "ATWc1",
        coal_price,
        None,
        None,
        None,
        None,
        today
    ])

    co2_price = scrape_investing_price(
        "https://www.investing.com/commodities/carbon-emissions"
    )

    rows.append([
        "CO2_EUA",
        "EUA",
        co2_price,
        None,
        None,
        None,
        None,
        today
    ])

    print("📊 Kerätyt rivit:")
    for r in rows:
        print(r)

    # =========================
    # ✅ WRITE latest_fuels.csv
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
    # ✅ HISTORY (yöllä)
    # =========================

    if not (2 <= hour <= 6):
        print("⏭️ ei tallenneta historyyn (ei yöajo)")
        return

    file_exists = os.path.isfile("historical_fuels.csv")

    if file_exists:
        try:
            hist = pd.read_csv("historical_fuels.csv")
            hist["Date"] = hist["Date"].astype(str)

            if today in hist["Date"].values:
                print("⏭️ history jo olemassa tältä päivältä")
                return
        except Exception as e:
            print(f"⚠️ history read error: {e}")

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
# ✅ TÄMÄ OLI PUUTTUVA OSA
# =========================
if __name__ == "__main__":
    scrape_fuels()
