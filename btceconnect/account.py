from collections import namedtuple


class Account:
    """Structure btc-e account model

    funds: Your account balance available for trading. Doesn’t include funds on your open orders.
    rights: The privileges of the current API key. At this time the privilege to withdraw is not used anywhere.
    transaction_count: Deprecated, is equal to 0.
    open_orders: The number of your open orders.
    server_time: Server time (MSK).

        {
        "success":1,
        "return":{
            "funds":{
                "usd":325,
                "btc":23.998,
                "ltc":0,
                ...
            },
            "rights":{
                "info":1,
                "trade":0,
                "withdraw":0
            },
            "transaction_count":0,
            "open_orders":1,
            "server_time":1342123547
        }
    }
    """

    def __init__(self, get_info_response):
        self._Funds = namedtuple("Funds", [coin for coin in get_info_response["return"]["funds"].keys()])
        self._Rights = namedtuple("Rights", [right for right in get_info_response["return"]["rights"].keys()])
        self.update_account(get_info_response)

    def update_account(self, get_info_response):
        self.funds = self._Funds(**get_info_response["return"]["funds"])
        self.rights = self._Rights(**get_info_response["return"]["rights"])
        self.open_orders = get_info_response["return"]["open_orders"]
        self.transaction_count = get_info_response["return"]["transaction_count"]
        self.server_time = get_info_response["return"]["server_time"]

    def __str__(self):
        return "({}. usd: {}, eur: {}, open orders: {})".format(self.__class__.__name__, self.funds.usd, self.funds.eur,
                                                                self.open_orders)

    def __repr__(self):
        return "({}. usd: {}, eur: {}, open orders: {})".format(self.__class__.__name__, self.funds.usd, self.funds.eur,
                                                                self.open_orders)
