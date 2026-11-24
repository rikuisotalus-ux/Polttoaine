import requests
import csv
from datetime import datetime

URL = "https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/8378/FUT"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.cmegroup.com/markets/energy/natural-gas/dutch-ttf-natural-gas-calendar-month.settlements.html",
    "Accept": "application/json"
}


def build_product_code(month):
    """
    DEC 26 -> TTFDEC-26
    JAN 27 -> TTFJAN-27
    """

    try:
        mon, yy = month.split()
        return f"TTF{mon.upper()}-{yy}"
    except:
        return None


def scrape_cme_ttf():

    params = {
        "strategy": "DEFAULT",
        "pageSize": 500
    }

    response = requests.get(
        URL,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    print("STATUS:", response.status_code)

    data = response.json()

    settlements = data.get("settlements", [])

    today = datetime.utcnow().strftime("%Y-%m-%d")

    rows = []

    for item in settlements:

        rows.append([
            item.get("month"),
            item.get("settle"),
            item.get("open"),
            item.get("high"),
            item.get("low"),
            item.get("last"),
            item.get("change"),
            item.get("volume"),
            item.get("openInterest"),
            "TTF",
            build_product_code(item.get("month", "")),
            today
        ])

    with open(
        "cme_ttf_settlement.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Delivery",
            "Settlement",
            "Open",
            "High",
            "Low",
            "Last",
            "Change",
            "Volume",
            "OpenInterest",
            "Product",
            "ProductCode",
            "Date"
        ])

        writer.writerows(rows)

    print(f"✓ {len(rows)} riviä tallennettu")


if __name__ == "__main__":
    scrape_cme_ttf()
