"""Unittest module"""
import unittest
import requests
from flask import Flask
from extention import db
from models import URL
from shortcode import read, get_stats


class TestShortcode(unittest.TestCase):
    """Test Shortcode """
    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_read_success(self):
        """read shortcode, success"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = URL(shortcode=shortcode, url=url)
        db.session.add(existing_shortcode)
        db.session.commit()
        response = read(shortcode)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], url)

    def test_read_notfound(self):
        """read shortcode, not found"""
        url ="http://127.0.0.1:7006/api/123"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 404)

    def test_getstats_notfound(self):
        """get shortcode stats, fail"""
        url ="http://127.0.0.1:7006/api/abc/stats"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 404)

    def test_getstats_success(self):
        """get shortcode stats, success"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = URL(shortcode=shortcode, url=url)
        db.session.add(existing_shortcode)
        db.session.commit()
        response = get_stats(shortcode)
        self.assertIsNotNone(response)

    def test_create_invalid_shortcode(self):
        """create shortcode, invalid shortcode"""
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "abc@#",
                "url": "www.sample.com"
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 412)

    def test_create_url_isnull(self):
        """create shortcode, url is null"""
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "abc@#",
                "url": ""
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate_shortcode(self):
        """create shortcode, duplicate shortcode"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = URL(shortcode=shortcode, url=url)
        db.session.add(existing_shortcode)
        db.session.commit()
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "abc123",
                "url": "http://sample.com"
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 409)

    def test_create_invalid_url(self):
        """create shortcode, duplicate shortcode"""
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "test",
                "url": "www.sample.com"
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 412)

    def test_create_duplicate_url(self):
        """create shortcode, duplicate shortcode"""
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "test",
                "url": "www.sample.com"
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 412)

if __name__ == "__main__":
    unittest.main()
