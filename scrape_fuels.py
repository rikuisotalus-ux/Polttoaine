import csv
import requests
import yfinance as yf
from datetime import datetime


# =========================
# ✅ Yahoo (oil + gas)
# =========================
def get_yahoo(symbol):
    try:
        data = yf.Ticker(symbol).history(period="2d")
        if len(data) >= 1:
            return float(data["Close"].iloc[-1])
    except Exception as e:
        print(f"Yahoo error {symbol}: {e}")
    return None


# =========================
# ✅ COAL (API2 MARKETWATCH CSV)
# =========================
def get_coal():
    try:
        url = "https://www.marketwatch.com/investing/future/mtfc00/download-data"

        r = requests.get(url, timeout=10)

        lines = r.text.splitlines()

        # viimeinen rivi = uusin data
        last_line = lines[-1].split(",")

        # Close hinta
        price = float(last_line[1])

        return price

    except Exception as e:
        print("Coal error:", e)
        return None


# =========================
# ✅ CO2 (EUA BUSINESS INSIDER)
# =========================
def get_co2():
    try:
        url = "https://markets.businessinsider.com/commodities/co2-european-emission-allowances"

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        import re

        match = re.search(r'"price":([0-9\.]+)', r.text)

        if match:
            return float(match.group(1))

    except Exception as e:
        print("CO2 error:", e)

    return None


# =========================
# ✅ MAIN
# =========================
def run():

    today = datetime.utcnow().strftime("%Y-%m-%d")

    rows = []

    # ✅ Oil & gas
    symbols = {
        "WTI": "CL=F",
        "BRENT": "BZ=F",
        "TTF": "TTF=F"
    }

    for name, symbol in symbols.items():
        price = get_yahoo(symbol)
        rows.append([name, symbol, price, today])

    # ✅ Coal
    coal_price = get_coal()
    rows.append(["COAL_API2", "MTFC00", coal_price, today])

    # ✅ CO2
    co2_price = get_co2()
    rows.append(["CO2_EUA", "EUA", co2_price, today])

    # ✅ Write CSV
    with open("latest_fuels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Product", "Symbol", "Price", "Date"])
        writer.writerows(rows)

    print("✅ DONE")
    for r in rows:
        print(r)


# =========================
if __name__ == "__main__":
    run()
