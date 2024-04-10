"""Shortener Module"""
import random
import string
import logging
import pathlib
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Database setup
basedir = pathlib.Path(__file__).parent.resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'shortener.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Logger setup
def create_logger():
    """Create logger"""
    log = logging.getLogger("__name__")
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(message)s %(levelname)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    return log

logger = create_logger()

# Model setup
class ShortCodes(db.Model):
    """URL Model"""
    __tablename__ = "shortcode"
    id_ = db.Column(db.Integer, primary_key=True)
    shortcode = db.Column(db.String(6), unique =True)
    url = db.Column(db.String(150))
    shortened_url= db.Column(db.String(100), unique = True)
    created_date = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    last_redirect = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    redirect_count = db.Column(db.Integer)

@app.route("/")
def display_home():
    """Renders the home page"""
    urls = ShortCodes.query.all()
    return render_template("home.html", urls = urls)

@app.route("/shorten", methods=["POST"])
def create_shortcode():
    """Create new shorten code"""
    data = request.json
    logger.info("create new shortcode for %s", data.get("url"))
    long_url = data.get("url")
    code = data.get("shortcode")
    if not long_url:
        logger.error("url is empty")
        return abort(400, "Url not present")
    if not long_url.startswith("http") or len(long_url) > 150:
        logger.error("url is invalid")
        return abort(412, "The provided url is invalid")
    if not code:
        code = get_random_code()
    if not validate_code(code):
        logger.error("shortcode is invalid")
        return abort(412, "The provided shortcode is invalid")
    existing_shortcode = ShortCodes.query.filter(ShortCodes.shortcode == code).first()
    if existing_shortcode is not None:
        logger.error("duplicate shortcode found")
        return abort(409, "Shortcode already in use")
    shortend_url = generate_shortened_url(long_url, code)
    new_shortcode = ShortCodes(shortcode=code, url=long_url, shortened_url=shortend_url,
                               created_date=datetime.now(), last_redirect=None, redirect_count=0)
    with db.session() as session:
        session.add(new_shortcode)
        session.commit()
    logger.info("successfully create new shortcode: %s for url %s", code, long_url)
    return jsonify({"shortcode": code}), 201

@app.route("/<shortcode>", methods=["GET"])
def read_shortcode(shortcode):
    """Endpoint to read shortcode information"""
    logger.info("read date by shortcode: %s", shortcode)
    existing_shortcode = ShortCodes.query.filter(ShortCodes.shortcode == shortcode).one_or_none()
    if existing_shortcode is None:
        return abort(404, "Shortcode not found")
    existing_shortcode.last_redirect = datetime.now()
    if existing_shortcode.redirect_count is not None:
        existing_shortcode.redirect_count += 1
    with db.session() as session:
        session.add(existing_shortcode)
        session.commit()
        response = make_response("", 302)
        response.headers['Location'] = existing_shortcode.url
        return response

@app.route("/<shortcode>/stats", methods=["GET"])
def get_stats_shortcode(shortcode):
    """Endpoint to retrieve statistics for the specified shortcode"""
    logger.info("get stats by shortcode: %s", shortcode)
    existing_shortcode = ShortCodes.query.filter(ShortCodes.shortcode == shortcode).one_or_none()
    if existing_shortcode:
        create_date = existing_shortcode.created_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        last_redirect = existing_shortcode.last_redirect.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        result = {"created": create_date,
                  "lastRedirect": last_redirect,
                  "redirectCount": existing_shortcode.redirect_count}
        return jsonify(result), 200
    return abort(404, "Shortcode not found")

def get_random_code():
    """Generate random alphanumeric characters with a length of 6"""
    return "".join(random.choices(string.ascii_letters + string.digits , k=6))

def validate_code(code):
    """Validate shortcode"""
    if not code:
        return False
    if len(code) != 6:
        return False
    if code.isalnum() or "_" in code:
        return True
    return False

def generate_shortened_url(url, shortcode):
    """Generate short url"""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/"
    return base_url + shortcode


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7006, debug=True)
