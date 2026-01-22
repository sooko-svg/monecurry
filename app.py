from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

app = Flask(__name__)

def fetch_prices():
    URL = "https://bonbast.com"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    r = requests.get(URL, headers=headers, timeout=15)
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
        else:
            data["prices"][name] = "N/A"

    with open("prices.json", "w") as f:
        json.dump(data, f)

    return data


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Bonbast Prices</title>
</head>
<body>
<h2>Bonbast Sell Prices</h2>
<table border="1" cellpadding="8">
<tr><th>Currency</th><th>Sell Price</th></tr>
{% for c,p in prices.items() %}
<tr>
<td>{{ c }}</td>
<td>{{ p }}</td>
</tr>
{% endfor %}
</table>
<p>Last update: {{ updated }}</p>
</body>
</html>
"""

@app.route("/")
def index():
    data = fetch_prices()
    return render_template_string(
        HTML,
        prices=data["prices"],
        updated=data["updated_at"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
