import http.client
import json
import urllib.error
import urllib.parse
import urllib.request

import hashlib
import hmac


class APIResponseError(Exception):
    """APIResponseError will be raised when BTC-e API returns a json response with a key named 'error'"""

    def __init__(self, *args, **kwargs):
        self._api_message = args[0]
        Exception.__init__(self, args, kwargs)

    def __str__(self):
        return self._api_message


class APIRequestHandler:
    """Manages all http POST and GET requests to the BTC-e API"""
    # BTC-e URLs:
    PUBLIC_INFO_URL = "https://btc-e.com/api/3/info"
    PUBLIC_TICKER_URL = "https://btc-e.com/api/3/ticker/"
    PUBLIC_DEPTH_URL = "https://btc-e.com/api/3/depth/"
    PUBLIC_TRADES_URL = "https://btc-e.com/api/3/trades/"

    def __init__(self, secret, key):
        self._KEY = key
        self._SECRET = secret

    def __str__(self):
        return "({})".format(self.__class__.__name__)

    def __repr__(self):
        return "({})".format(self.__class__.__name__)

    def _sign(self, params, secret):
        """Sings btc-e api secret key to authenticate to BTC-e API"""
        parameters = hmac.new(key=secret.encode(), digestmod=hashlib.sha512)
        parameters.update(params.encode("utf-8"))
        sign = parameters.hexdigest()
        return sign

    @staticmethod
    def _parse_json(json_data):
        try:
            return json.loads(json_data)
        except json.JSONDecodeError as error:
            raise APIResponseError(error)

    def request_trade_api(self, params):
        """Sends a http POST request to the btc-e trade api and returns back response in dictionary format.
            If there is an 'error' key in the response an APIResponseError Exception will be raised."""
        params = urllib.parse.urlencode(params)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Key": self._KEY,
                   "Sign": self._sign(params, self._SECRET)}
        connection = http.client.HTTPSConnection("btc-e.com", timeout=60)
        connection.request("POST", "/tapi", params, headers)
        parsed_json_data = APIRequestHandler._parse_json(connection.getresponse().read().decode())
        try:
            error = parsed_json_data["error"]
        except KeyError:
            return parsed_json_data
        else:
            raise APIResponseError(error)

    @staticmethod
    def request_public_api(url):
        """Sends a http GET request to the btc-e public api and returns back response in dictionary format.
            If there is an 'error' key in the response an APIResponseError Exception will be raised."""
        response = urllib.request.urlopen(url=url)
        response = response.read()
        decoded_response = response.decode()
        parsed_json_data = APIRequestHandler._parse_json(decoded_response)
        try:
            error = parsed_json_data["error"]
        except KeyError:
            return parsed_json_data
        else:
            raise APIResponseError(error)
