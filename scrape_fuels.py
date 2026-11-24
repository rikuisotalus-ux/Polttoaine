import requests

url = "https://www.barchart.com/proxies/core-api/v1/quotes/get"

params = {
    "symbol": "TG^F",
    "fields": (
        "symbol,contractName,lastPrice,"
        "priceChange,highPrice,lowPrice,volume"
    ),
    "raw": 1,
    "limit": 6
}

r = requests.get(url)

print("STATUS:", r.status_code)
print(r.text[:1000])
