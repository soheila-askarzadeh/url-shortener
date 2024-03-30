"""Shortener Module"""
import extention
from flask import render_template
from models import URL

app = extention.connex_app
app.add_api(extention.basedir / "swagger.yml")

@app.route("/")
def display_home():
    """Renders the home page"""
    urls = URL.query.all()
    return render_template("home.html", urls = urls)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7006, debug=True)
