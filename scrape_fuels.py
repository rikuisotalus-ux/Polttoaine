import requests

url = "https://www.cmegroup.com/CmeWS/mvc/Settlements/Futures/Settlements/8378/FUT"

params = {
    "strategy": "DEFAULT",
    "pageSize": 500
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.cmegroup.com/markets/energy/natural-gas/dutch-ttf-natural-gas-calendar-month.settlements.html"
}

r = requests.get(
    url,
    params=params,
    headers=headers,
    timeout=30
)

print("STATUS:", r.status_code)
print(r.text[:2000])
