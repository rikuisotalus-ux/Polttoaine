import csv
import requests
from datetime import datetime

URL = "https://scanner.tradingview.com/futures/scan"

MONTH_CODES = {
    1: "F",
    2: "G",
    3: "H",
    4: "J",
    5: "K",
    6: "M",
    7: "N",
    8: "Q",
    9: "U",
    10: "V",
    11: "X",
    12: "Z"
}


def next_contract_symbol():
    now = datetime.utcnow()

    month = now.month + 1
    year = now.year

    if month > 12:
        month = 1
        year += 1

    return f"NYMEX:TTF{MONTH_CODES[month]}{year}"


def fetch_symbol(symbol):

    payload = {
        "symbols": {
            "tickers": [symbol],
            "query": {
                "types": []
            }
        },
        "columns": [
            "name",
            "close",
            "change"
        ]
    }

    response = requests.post(
        URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data.get("data"):
        return None

    row = data["data"][0]

    if not row.get("d"):
        return None

    values = row["d"]

    if len(values) < 3:
        return None

    if values[1] is None:
        return None

    return {
        "contract": values[0],
        "price": values[1],
        "change_pct": values[2]
    }


def main():

    data = fetch_symbol("NYMEX:TTF1!")

    source_symbol = "NYMEX:TTF1!"

    if data is None:

        fallback = next_contract_symbol()

        data = fetch_symbol(fallback)

        source_symbol = fallback

    if data is None:
        raise Exception(
            "TTF-dataa ei löytynyt TradingViewsta."
        )

    today = datetime.utcnow().strftime("%Y-%m-%d")

    with open(
        "latest_fuels.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Date",
            "Price",
            "ChangePct"
        ])

        writer.writerow([
            today,
            data["price"],
            data["change_pct"]
        ])

    print(
        f"Source={source_symbol} | "
        f"Contract={data['contract']} | "
        f"Price={data['price']} | "
        f"Change={data['change_pct']}%"
    )


if __name__ == "__main__":
    main()
