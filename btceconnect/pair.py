from collections import namedtuple


class PairNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)

    def __repr__(self):
        return "{}: {}".format(PairNotFoundError, self.message)


class Pair:
    """Creates BTC-e api Pair data model from the public api methos: info and ticker"""

    def __init__(self, pair_name, public_info_response, ticker_response):
        self._Ticker = namedtuple("Ticker", ["avg", "buy", "high", "last", "low", "sell", "updated", "vol", "vol_cur"])
        self._Info = namedtuple("Info", ["max_price", "min_amount", "hidden", "min_price", "fee", "decimal_places"])
        self.name = pair_name
        self.update_pair(public_info=public_info_response, ticker=ticker_response)

    @staticmethod
    def get_available_pairs(public_info):
        """Returns a list of the current available pairs. It can be that for determinated reason, BTC-e API remove
            removes an offered trading pair.
        """
        return [pair for pair in public_info["pairs"].keys()]

    def update_pair(self, public_info, ticker):
        """Updates pair's attributes using public info and ticker responses"""
        try:
            self.info = self._Info(**public_info["pairs"][self.name])
            self.ticker = self._Ticker(**ticker[self.name])
        except KeyError as e:
            raise PairNotFoundError(e)

    def __repr__(self):
        return "({}. name: {}, buy: {}, sell: {}, fee: {})".format(self.__class__.__name__, self.name, self.ticker.buy,
                                                                   self.ticker.sell, self.info.fee)

    def __len__(self):
        """Returns an integer of pair shares traded during a given period of time."""
        return int(self.ticker.vol)
