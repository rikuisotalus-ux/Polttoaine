import requests
import json

URL = "https://scanner.tradingview.com/futures/scan"

payload = {
    "symbols": {
        "tickers": [
            "NYMEX:TTFZ2026"
        ],
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

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

r = requests.post(
    URL,
    json=payload,
    headers=headers,
    timeout=30
)

print("STATUS:", r.status_code)
print(r.text[:5000])
