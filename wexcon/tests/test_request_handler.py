import unittest

from wexcon.request_handler import APIRequestHandler
from wexcon.request_handler import APIResponseError


class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.invalid_api_key = "this is my key"
        self.invalid_api_secret = "this is my secret"
        self.nonce = 10
        self.method = "getInfo"
        self.handler = APIRequestHandler(self.invalid_api_secret, self.invalid_api_key)

    def test_sign_checkHmac_SHA512signatureValidity(self):
        params = "nonce={}&method={}".format(self.nonce, self.method)
        signature = self.handler._sign(params, self.invalid_api_secret)
        expected = "a1f24c97a833e22ff8e803a614790351e9b62ee5c8ecec3e897fd8d2aa628" \
                   "305206722983c390ea0433449a65d678501636ec810943765bb0cd955c407dfa698"
        self.assertEqual(expected, signature, msg="invalid signature")

    def test_request_trade_api_raiseAPIResponseError(self):
        params = {"nonce": 0, "method": "getInfo"}
        with self.assertRaises(APIResponseError):
            self.handler.request_trade_api(params=params)

    def test_request_public_api_raiseAPIResponseErrorWithBadURL(self):
        bad_url = "https://wex.nz/api/3/ticker/btc_usd-btc7"
        expected_exception_message = 'Invalid pair name: btc7'
        with self.assertRaises(APIResponseError) as error:
            self.handler.request_public_api(bad_url)
        exception_message = error.exception._api_message
        self.assertEqual(expected_exception_message, exception_message)

    def test_request_public_api_checkForSuccessfulRequest(self):
        url = "https://wex.nz/api/3/ticker/btc_usd"
        response = self.handler.request_public_api(url)
        self.assertIsInstance(response, dict)


if __name__ == "__main__":
    unittest.main()
