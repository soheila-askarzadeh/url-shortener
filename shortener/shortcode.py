"""Short codes information"""
import random
import string
import logging
from datetime import datetime
from extention import db
from flask import abort, make_response, jsonify
from models import URL

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

def create(url):
    """Create new shorten code"""
    logger.info("create new shortcode for %s",url)
    long_url = url.get("url")
    code = url.get("shortcode")
    if not long_url:
        logger.error("url is empty")
        return abort(400, "Url not present")
    if not long_url.startswith("http"):
        logger.error("url is invalid")
        return abort(412, "The provided url is invalid")
    if not code:
        code = get_random_code()
    if not validate_code(code):
        logger.error("shortcode is invalid")
        return abort(412, "The provided shortcode is invalid")
    existing_shortcode = URL.query.filter(URL.shortcode == code).first()
    if existing_shortcode is not None:
        logger.error("duplicate shortcode found")
        return abort(409, "Shortcode already in use")
    existing_shortcode = URL.query.filter(URL.url == long_url).first()
    if existing_shortcode is not None:
        logger.error("duplicate url found")
        return abort(409, "url already in use")
    new_shortcode = URL(shortcode=code, url=long_url,
                 createDate=datetime.now(), lastRedirect=None, redirectCount=0)
    db.session.add(new_shortcode)
    db.session.commit()
    logger.info("successfully create new shortcode: %s for url %s", code, long_url)
    return jsonify({"shortcode": code}), 201

def get_random_code():
    """Generate random alphanumeric characters with a length of 6"""
    return "".join(random.choices(string.ascii_letters + string.digits , k=6))

def validate_code(code):
    """Validate shortcode"""
    if not code:
        return False
    if code.isalnum() or "_" in code:
        return True
    return False

def read(shortcode):
    """Read one shortcode"""
    logger.info("read date by shortcode: %s",shortcode)
    existing_shortcode = URL.query.filter(URL.shortcode == shortcode).one_or_none()
    if existing_shortcode is None:
        return abort(404, "Shortcode not found")
    existing_shortcode.lastRedirect = datetime.now()
    if existing_shortcode.redirectCount is not None:
        existing_shortcode.redirectCount += 1
    try:
        db.session.commit()
    except Exception as e:
        logger.error("Failed to commit changes to database: %s", e)
        db.session.rollback()
        return abort(500, "Internal Server Error")
    response = make_response("", 302)
    response.headers['Location'] = existing_shortcode.url
    return response

def get_stats(shortcode):
    """Retrieves statistics for the specified shortcode"""
    logger.info("get stats by shortcode: %s",shortcode)
    existing_shortcode = URL.query.filter(URL.shortcode == shortcode).one_or_none()
    if existing_shortcode:
        create_date = existing_shortcode.createDate.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        last_redirect = existing_shortcode.lastRedirect.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
        result = {"created": create_date,
                  "lastRedirect": last_redirect,
                  "redirectCount":existing_shortcode.redirectCount}
        return jsonify(result), 200
    return abort(404,"Shortcode not found")
