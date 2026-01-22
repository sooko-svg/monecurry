from flask import Flask, render_template_string
import json

app = Flask(__name__)

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
  <td>{{ "{:,}".format(int(p)) }}</td>
</tr>
{% endfor %}
</table>
<p>Last update: {{ updated }}</p>
</body>
</html>
"""

@app.route("/")
def index():
    with open("prices.json") as f:
        data = json.load(f)
    return render_template_string(
        HTML,
        prices=data["prices"],
        updated=data["updated_at"]
    )

if __name__ == "__main__":
    app.run()
