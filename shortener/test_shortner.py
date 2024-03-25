"""Unittest module"""
import unittest
import requests

class TestShortcode(unittest.TestCase):
    """Test Shortcode """
    def test_read_success(self):
        """read shortcode, success"""
        url ="http://127.0.0.1:7006/api/abc123"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 302)

    def test_read_notfound(self):
        """read shortcode, not found"""
        url ="http://127.0.0.1:7006/api/123"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 404)

    def test_getstats_success(self):
        """get shortcode stats, success"""
        url ="http://127.0.0.1:7006/api/abc123/stats"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 200)

    def test_getstats_notfound(self):
        """get shortcode stats, fail"""
        url ="http://127.0.0.1:7006/api/abc/stats"
        response = requests.get(url, timeout= 10)
        self.assertEqual(response.status_code, 404)

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
        url ="http://127.0.0.1:7006/api/shorten"
        payload ={
                "shortcode": "abc123",
                "url": "www.sample.com"
                }
        response = requests.post(url, json = payload, timeout = 10)
        self.assertEqual(response.status_code, 409)

if __name__ == "__main__":
    unittest.main()
