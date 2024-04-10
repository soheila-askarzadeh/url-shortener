"""Unittest module"""
import unittest
from app import app, db, ShortCodes

class TestShortcode(unittest.TestCase):
    """Test Shortcode """
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_read_success(self):
        """read shortcode, success"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = ShortCodes(shortcode=shortcode, url=url)
        with app.app_context():
            db.session.add(existing_shortcode)
            db.session.commit()
        response = self.app.get(f'/{shortcode}')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers['Location'], url)

    def test_read_notfound(self):
        """read shortcode, not found"""
        response = self.app.get('/123')
        self.assertEqual(response.status_code, 404)

    def test_getstats_notfound(self):
        """get shortcode stats, not found"""
        response = self.app.get('/abc123/stats')
        self.assertEqual(response.status_code, 404)

    def test_getstats_success(self):
        """get shortcode stats, success"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = ShortCodes(shortcode=shortcode, url=url)
        with app.app_context():
            db.session.add(existing_shortcode)
            db.session.commit()
        response = self.app.get(f'/{shortcode}/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json)

    def test_create_invalid_shortcode(self):
        """create shortcode, invalid shortcode"""
        payload = {
            "shortcode": "abc@#",
            "url": "http://www.sample.com"
        }
        response = self.app.post('/shorten', json=payload)
        self.assertEqual(response.status_code, 412)

    def test_create_url_isnull(self):
        """create shortcode, url is null"""
        payload = {
            "shortcode": "abc123",
            "url": ""
        }
        response = self.app.post('/shorten', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate_shortcode(self):
        """create shortcode, duplicate shortcode"""
        shortcode = 'abc123'
        url = 'http://example.com'
        existing_shortcode = ShortCodes(shortcode=shortcode, url=url)
        with app.app_context():
            db.session.add(existing_shortcode)
            db.session.commit()
        payload = {
            "shortcode": "abc123",
            "url": "http://www.sample.com"
        }
        response = self.app.post('/shorten', json=payload)
        self.assertEqual(response.status_code, 409)

    def test_create_invalid_url(self):
        """create shortcode, invalid url"""
        payload = {
            "shortcode": "test",
            "url": "www.sample.com"
        }
        response = self.app.post('/shorten', json=payload)
        self.assertEqual(response.status_code, 412)

if __name__ == "__main__":
    unittest.main()
