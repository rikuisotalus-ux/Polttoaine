import requests

url = "https://www.barchart.com/proxies/core-api/v1/quotes/get"

params = {
    "symbol": "TG^F",
    "fields": "symbol,contractName,lastPrice"
}

r = requests.get(url)

print(r.status_code)
print(r.text[:1000])
