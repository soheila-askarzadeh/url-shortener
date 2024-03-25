"""Shortener Module"""
import extention

app = extention.connex_app
app.add_api(extention.basedir / "swagger.yml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7006, debug=True)
