class Ticker:
    """ BTC-e Ticker Data """

    def __init__(self, pair_name, ticker_response):
        self.name = pair_name
        ticker_data = ticker_response.get(self.name)
        for tick_attribute in ["avg", "buy", "high", "last", "low", "sell", "updated", "vol", "vol_cur"]:
            self.__setattr__(tick_attribute, ticker_data[tick_attribute])

    def __str__(self):
        return "<{}> pair: {} buy: {} sell: {}".format(self.__class__.__name__, self.name, self.buy, self.sell)


class PublicInfo:
    """ BTC-e trading public information """

    def __init__(self, pair_name, public_info):
        self.name = pair_name
        public_info_data = public_info["pairs"][self.name]
        for info_attribute in ["max_price", "min_amount", "hidden", "min_price", "fee", "decimal_places"]:
            self.__setattr__(info_attribute, public_info_data[info_attribute])

    def __str__(self):
        return "<{}> pair: {} fee: {}".format(self.__class__.__name__, self.name, self.fee)


class PairNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        Exception.__init__(self, self.message)

    def __repr__(self):
        return "{}: {}".format(PairNotFoundError, self.message)


class Pair:
    """ Creates BTC-e api Pair data model from the public api methods:
     info and ticker"""

    def __init__(self, pair_name, public_info_response, ticker_response):
        self.name = pair_name
        try:
            self.ticker = Ticker(self.name, ticker_response)
            self.info = PublicInfo(self.name, public_info_response)
        except KeyError as e:
            raise PairNotFoundError(e)

    @staticmethod
    def get_available_pairs(public_info):
        """ Returns a list of the current available pairs. It can 
        be that for determinated reason, BTC-e API remove removes
        an offered trading pair. """
        return [pair for pair in public_info["pairs"].keys()]

    def update_pair(self, public_info, ticker):
        """ Updates pair's attributes using public info and ticker
         responses """
        try:
            self.info = PublicInfo(self.name, public_info)
            self.ticker = Ticker(self.name, ticker)
        except KeyError as e:
            raise PairNotFoundError(e)

    def __repr__(self):
        return "({}. name: {}, buy: {}, sell: {}, fee: {})".format(self.__class__.__name__, self.name, self.ticker.buy,
                                                                   self.ticker.sell, self.info.fee)

    def __len__(self):
        """ Returns an integer of pair shares traded during a 
        given period of time """
        return int(self.ticker.vol)
