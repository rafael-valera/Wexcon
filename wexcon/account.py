class AccountRights:
    """ Account rights """

    def __init__(self, get_info_response):
        self.account_data = get_info_response["return"]["rights"]

    @property
    def info(self):
        return self.account_data.get("info")

    @property
    def trade(self):
        return self.account_data.get("trade")

    @property
    def withdraw(self):
        return self.account_data.get("withdraw")


class AccountFunds:
    """ Account funds """

    def __init__(self, get_info_response):
        funds = get_info_response["return"]["funds"]
        expected = [coin for coin in funds.keys()]
        for coin in expected:
            self.__setattr__(coin, funds.get(coin))


class AccountInfo:
    """ Account's server time, open orders and transaction count """

    def __init__(self, get_info_response):
        self.info = get_info_response["return"]

    @property
    def open_orders(self):
        return self.info.get("open_orders")

    @property
    def transaction_count(self):
        return self.info.get("transaction_count")

    @property
    def server_time(self):
        return self.info.get("server_time")


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
        self.rights = AccountRights(get_info_response)
        self.funds = AccountFunds(get_info_response)
        self.info = AccountInfo(get_info_response)

    def update_account(self, get_info_response):
        self.__init__(get_info_response)

    def __str__(self):
        return "({}. usd: {}, eur: {}, open orders: {})".format(self.__class__.__name__, self.funds.usd, self.funds.eur,
                                                                self.info.open_orders)

    def __repr__(self):
        return self.__str__()
