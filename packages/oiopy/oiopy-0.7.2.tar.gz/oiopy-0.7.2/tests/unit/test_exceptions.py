import unittest

from oiopy import exceptions
from oiopy import fakes


class ExceptionsTest(unittest.TestCase):
    def test_from_response(self):
        fake_resp = fakes.FakeResponse()
        fake_resp.status_code = 500
        exc = exceptions.from_response(fake_resp, None)
        self.assertTrue(isinstance(exc, exceptions.ClientException))
        self.assertEqual(exc.http_status, fake_resp.status_code)
        self.assertEqual(exc.message, "n/a")
        self.assertTrue("HTTP 500" in str(exc))

    def test_from_response_with_body(self):
        fake_resp = fakes.FakeResponse()
        fake_resp.status_code = 500
        body = {"status": 300, "message": "Fake error"}
        exc = exceptions.from_response(fake_resp, body)
        self.assertTrue(isinstance(exc, exceptions.ClientException))
        self.assertEqual(exc.http_status, fake_resp.status_code)
        self.assertEqual(exc.status, 300)
        self.assertEqual(exc.message, "Fake error")
        self.assertTrue("HTTP 500" in str(exc))
        self.assertTrue("STATUS 300" in str(exc))

    def test_from_response_http_status(self):
        fake_resp = fakes.FakeResponse()
        fake_resp.status_code = 404
        exc = exceptions.from_response(fake_resp, None)
        self.assertTrue(isinstance(exc, exceptions.NotFound))
        fake_resp.status_code = 409
        exc = exceptions.from_response(fake_resp, None)
        self.assertTrue(isinstance(exc, exceptions.Conflict))
