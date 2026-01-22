import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

URL = "https://bonbast.com"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(URL, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

currencies = {
    "USD": "usd1",
    "EUR": "eur1",
    "GBP": "gbp1",
    "AED": "aed1",
    "TRY": "try1"
}

data = {
    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "prices": {}
}

for name, cid in currencies.items():
    el = soup.find(id=cid)
    if el:
        data["prices"][name] = el.text.replace(",", "").strip()

with open("prices.json", "w") as f:
    json.dump(data, f)

print("OK")

