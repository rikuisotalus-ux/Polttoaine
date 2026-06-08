def scrape_fuels():

    import requests
    import csv
    import os
    import pandas as pd
    from datetime import datetime
    from bs4 import BeautifulSoup
    import yfinance as yf

    today = datetime.utcnow().strftime("%Y-%m-%d")
    hour = datetime.utcnow().hour

    rows = []

    # =========================
    # ✅ YAHOO SYMBOLIT
    # =========================
    YAHOO_SYMBOLS = {
        "WTI_OIL": "CL=F",
        "BRENT_OIL": "BZ=F",
        "TTF_GAS": "TTF=F",   # ✅ oikea
        "CO2": "KRBN",        # proxy
        "COAL": "KOL"         # proxy fallback
    }

    # =========================
    # ✅ INVESTING (oikeat tuotteet)
    # =========================
    INVESTING_URLS = {
        "COAL_API2": "https://www.investing.com/commodities/rotterdam-coal-futures",
        "CO2_EUA": "https://www.investing.com/commodities/carbon-emissions"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # =========================
    # ✅ YAHOO HAKU
    # =========================

    for name, symbol in YAHOO_SYMBOLS.items():

        print(f"🔎 Yahoo: {name}")

        last_price = None

        try:
            data = yf.Ticker(symbol).history(period="1d")

            if not data.empty:
                last_price = float(data["Close"].iloc[-1])

        except Exception as e:
            print(f"⚠️ Yahoo fail {name}: {e}")

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

    # =========================
    # ✅ INVESTING SCRAPER
    # =========================

    def scrape_investing(url):
        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            price = soup.find("span", {"data-test": "instrument-price-last"})

            if price:
                return float(price.text.replace(",", ""))
        except Exception as e:
            print(f"⚠️ Investing fail: {e}")

        return None

    # =========================
    # ✅ COAL API2 (oikea)
    # =========================

    coal_price = scrape_investing(INVESTING_URLS["COAL_API2"])

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

    # =========================
    # ✅ EUA (oikea)
    # =========================

    co2_price = scrape_investing(INVESTING_URLS["CO2_EUA"])

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

    # =========================
    # ✅ WRITE latest
    # =========================

    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Product", "Symbol", "Last", "Close",
            "PrevClose", "IntradayChange", "DailyChange", "Date"
        ])
        writer.writerows(rows)

    print("✅ latest_fuels.csv päivitetty")

    # =========================
    # ✅ HISTORY (YÖ)
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
