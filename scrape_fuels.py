import csv
import requests
from datetime import datetime

MONTH_CODES = {
    1: "F",  # Jan
    2: "G",  # Feb
    3: "H",  # Mar
    4: "J",  # Apr
    5: "K",  # May
    6: "M",  # Jun
    7: "N",  # Jul
    8: "Q",  # Aug
    9: "U",  # Sep
    10: "V", # Oct
    11: "X", # Nov
    12: "Z"  # Dec
}

URL = "https://scanner.tradingview.com/futures/scan"


def build_ttf_symbols(months_forward=36):
    """
    Luo automaattisesti seuraavat TTF-sopimukset
    esim.
    NYMEX:TTFZ2026
    NYMEX:TTFF2027
    ...
    """

    today = datetime.utcnow()

    symbols = []

    year = today.year
    month = today.month

    for i in range(months_forward):

        m = month + i
        y = year

        while m > 12:
            m -= 12
            y += 1

        code = MONTH_CODES[m]

        symbols.append(
            f"NYMEX:TTF{code}{y}"
        )

    return symbols


def extract_expiry(symbol):
    """
    NYMEX:TTFZ2026 -> (2026,12)
    """

    s = symbol.split(":")[1]

    month_code = s[3]
    year = int(s[4:])

    reverse_codes = {v: k for k, v in MONTH_CODES.items()}

    month = reverse_codes[month_code]

    return year, month


def contract_is_valid(symbol):
    """
    Poistaa vanhat sopimukset
    """

    year, month = extract_expiry(symbol)

    now = datetime.utcnow()

    current_value = now.year * 100 + now.month
    contract_value = year * 100 + month

    return contract_value >= current_value


def scrape_ttf():

    tickers = build_ttf_symbols(36)

    payload = {
        "symbols": {
            "tickers": tickers,
            "query": {
                "types": []
            }
        },
        "columns": [
            "name",
            "close",
            "change",
            "high",
            "low",
            "volume"
        ]
    }

    response = requests.post(
        URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    rows = []

    today = datetime.utcnow().strftime("%Y-%m-%d")

    for item in data.get("data", []):

        symbol = item.get("s")
        values = item.get("d", [])

        if not symbol:
            continue

        if not contract_is_valid(symbol):
            continue

        if len(values) < 6:
            continue

        contract = values[0]
        settlement = values[1]
        change_pct = values[2]
        high = values[3]
        low = values[4]
        volume = values[5]

        if settlement is None:
            continue

        if volume is None:
            continue

        rows.append([
            symbol,
            contract,
            settlement,
            change_pct,
            high,
            low,
            volume,
            today
        ])

    if not rows:
        raise Exception(
            "Ei löytynyt yhtään validia TTF-sopimusta."
        )

    rows.sort(key=lambda x: x[0])

    with open(
        "ttf_settlements.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "Symbol",
            "Contract",
            "Settlement",
            "ChangePct",
            "High",
            "Low",
            "Volume",
            "Date"
        ])

        writer.writerows(rows)

    print(f"✅ Tallennettu {len(rows)} sopimusta")

    for row in rows:
        print(
            f"{row[1]} | "
            f"Settlement={row[2]} | "
            f"Volume={row[6]}"
        )


if __name__ == "__main__":
    scrape_ttf()
