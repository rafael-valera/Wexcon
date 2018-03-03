from wexcon.pair import Pair
from wexcon.request_handler import APIRequestHandler, APIResponseError


class Trader:
    """
    API to query WEX server for public data and all common trading transactions
    """

    def __init__(self, key, secret):
        self._NONCE = 0
        self._api_handler = APIRequestHandler(key=key, secret=secret)
        self._set_nonce()

    def _get_nonce(self):
        self._NONCE += 1
        return self._NONCE

    def _set_nonce(self):
        """Sets up initial nonce number"""
        try:
            self.get_info()
        except APIResponseError as api_exception:
            error = api_exception.args[0][0]
            if "invalid nonce" in error:
                nonce = int(error.split(":")[3]) - 1
                self._NONCE = nonce
            else:
                raise

    def __str__(self):
        return "({}. at nonce: {})".format(self.__class__.__name__, self._NONCE)

    def __repr__(self):
        return "({}. at nonce: {})".format(self.__class__.__name__, self._NONCE)

    # PUBLIC API METHODS
    def depth_public(self, pairs, limit=30):
        """
        This method provides the information about active orders on the pair.
        Additionally it accepts an optional GET-parameter limit, which indicates how many orders
        should be displayed (150 by default). Is set to less than 2000.

        :returns
        asks: Sell orders.
        bids: Buy orders.
        """
        dept_formatted_url = self._api_handler.PUBLIC_DEPTH_URL + '-'.join(pairs) + "?limit={}".format(limit)
        return self._api_handler.request_public_api(url=dept_formatted_url)

    def ticker_public(self):
        """
        This method provides all the information about currently active pairs, such as:
        the maximum price, the minimum price, average price, trade volume, trade volume in currency,
        the last trade, Buy and Sell price. All information is provided over the past 24 hours.

        :returns
        high: maximum price.
        low: minimum price.
        avg: average price.
        vol: trade volume.
        vol_cur: trade volume in currency.
        last: the price of the last trade.
        buy: buy price.
        sell: sell price.
        updated: last update of cache.
        """

        dept_formatted_url = self._api_handler.PUBLIC_TICKER_URL + '-'.join(
            Pair.get_available_pairs(self.public_info()))
        return self._api_handler.request_public_api(url=dept_formatted_url)

    def public_trades(self, pairs, limit=30):
        """
        This method provides the information about the last trades.
        Additionally it accepts an optional GET-parameter limit, which indicates how many orders should be displayed.
        The maximum allowable value is 2000.

        :returns
        type: ask – Sell, bid – Buy.
        price: Buy price/Sell price.
        amount: the amount of asset bought/sold.
        tid: trade ID.
        timestamp: UNIX time of the trade.
        """
        dept_formatted_url = self._api_handler.PUBLIC_TRADES_URL + '-'.join(pairs) + "?limit={}".format(limit)
        return self._api_handler.request_public_api(url=dept_formatted_url)

    def public_info(self):
        """
        This method provides all the information about currently active pairs, such as:
        the maximum number of digits after the decimal point, the minimum price, the maximum price,
        the minimum transaction size, whether the pair is hidden, the commission for each pair.

        :returns
        decimal_places: number of decimals allowed during trading.
        min_price: minimum price allowed during trading.
        max_price: maximum price allowed during trading.
        min_amount: minimum sell / buy transaction size.
        hidden: whether the pair is hidden, 0 or 1.
        fee: commission for this pair.
        """
        return self._api_handler.request_public_api(url=self._api_handler.PUBLIC_INFO_URL)

    # TRADE API METHODS
    def get_info(self):
        """Returns information about the user’s current balance, API-key privileges,
        the number of open orders and Server Time. To use this method you need a privilege of the key info.

        :returns
        funds: Your account balance available for trading. Doesn’t include funds on your open orders.
        rights: The privileges of the current API key. At this time the privilege to withdraw is not used anywhere.
        transaction_count: Deprecated, is equal to 0.
        open_orders: The number of your open orders.
        server_time: Server time (MSK).
        """
        parameters = dict(nonce=self._get_nonce(), method="getInfo")
        return self._api_handler.request_trade_api(parameters)

    def trade(self, pair, trans_type, rate, amount):
        """The basic method that can be used for creating orders and trading on the exchange. To use this method
            you need an API key privilege to trade.

        :returns
        received: The amount of currency bought/sold.
        remains: The remaining amount of currency to be bought/sold (and the initial order amount).
        order_id: Is equal to 0 if the request was fully “matched” by the opposite orders,
            otherwise the ID of the executed order will be returned.
        funds: Balance after the request.
        """
        parameters = dict(nonce=self._get_nonce(), method="Trade", pair=pair, type=trans_type, rate=rate,
                          amount=amount)
        return self._api_handler.request_trade_api(parameters)

    def active_orders(self, pair):
        """
        Returns the list of your active orders. To use this method you need a privilege of the info key.

        :returns
        Array key : Order ID.
        pair: The pair on which the order was created.
        type: Order type, buy/sell.
        amount: The amount of currency to be bought/sold.
        rate: Sell/Buy price.
        timestamp_created: The time when the order was created.
        status: Deprecated, is always equal to 0
        """
        parameters = dict(nonce=self._get_nonce(), method="ActiveOrders", pair=pair)
        return self._api_handler.request_trade_api(parameters)

    def order_info(self, order_id):
        """
        Returns the information on particular order. To use this method you need a privilege of the info key.

        :returns
        Array key: Order ID.
        pair: The pair on which the order was created
        type: Order type, buy/sell.
        start_amount: The initial amount at the time of order creation.
        amount: The remaining amount of currency to be bought/sold.
        rate: Sell/Buy price.
        timestamp_created: The time when the order was created.
        status: 0 - active, 1 – executed order, 2 - canceled, 3 – canceled, but was partially executed.
        """
        parameters = dict(nonce=self._get_nonce(), method="OrderInfo", order_id=order_id)
        return self._api_handler.request_trade_api(parameters)

    def cancel_order(self, order_id):
        """
        This method is used for order cancelation. To use this method you need a privilege of the trade key.

        :returns
        order_id: The ID of canceled order.
        funds: Balance upon request.
        """
        parameters = dict(nonce=self._get_nonce(), method="CancelOrder", order_id=order_id)
        return self._api_handler.request_trade_api(parameters)

    def trade_history(self, from_order=0, count=1000, from_id=0, end_id=1000000000, order="DESC", since=0, pair=""):
        """
        Returns trade history. To use this method you need a privilege of the info key.

        :returns
        Array keys: Trade ID.
        pair: The pair on which the trade was executed.
        type: Trade type, buy/sell.
        amount: The amount of currency was bought/sold.
        rate: Sell/Buy price.
        order_id: Order ID.
        is_your_order: Is equal to 1 if order_id is your order, otherwise is equal to 0.
        timestamp: Trade execution time.
        """
        parameters = dict(nonce=self._get_nonce(), method="TradeHistory", from_order=from_order,
                          count=count, from_id=from_id, end_id=end_id, order=order, since=since, end="", pair=pair)
        return self._api_handler.request_trade_api(parameters)

    def transactions_history(self, from_order=0, count=1000, from_id=0, end_id=1000000000, order="DESC", since=0, ):
        """Returns the history of transactions. To use this method you need a privilege of the info key.

        :returns
        Array keys: Transaction ID.
        type: Transaction type. 1/2 - deposit/withdrawal, 4/5 - credit/debit.
        amount: Transaction amount.
        currency: Transaction currency.
        desc: Transaction description.
        status: Transaction status. 0 - canceled/failed, 1 - waiting for acceptance, 2 - successful, 3 – not confirmed
        timestamp: Transaction time.
        """
        parameters = dict(nonce=self._get_nonce(), method="TransHistory", from_order=from_order,
                          count=count, from_id=from_id, end_id=end_id, order=order, since=since, end="")
        return self._api_handler.request_trade_api(parameters)

    def withdraw_coin(self, coin, amount):
        """
        The method is designed for cryptocurrency withdrawals.
        Please note: You need to have the privilege of the Withdraw key to be able to use this method.
        You can make a request for enabling this privilege by submitting a ticket to Support.
        You need to create the API key that you are going to use for this method in advance.
        Please provide the first 8 characters of the key (e.g. HKG82W66) in your ticket to support.
        We'll enable the Withdraw privilege for this key.
        When using this method, there will be no additional confirmations of withdrawal.
        Please note that you are fully responsible for keeping the secret of the API key safe
            after we have enabled the Withdraw privilege for it.

        :returns
        tId: Transaction ID.
        amountSent: The amount sent including commission.
        funds: Balance after the request.
        """
        parameters = dict(nonce=self._get_nonce(), method="WithdrawCoin", coinName=coin, amount=amount,
                          address="")
        return self._api_handler.request_trade_api(parameters)

    def create_coupon(self, currency, amount):
        """
        This method allows you to create Coupons.
        Please, note: In order to use this method, you need the Coupon key privilege.
        You can make a request to enable it by submitting a ticket to Support..
        You need to create the API key that you are going to use for this method in advance.
        Please provide the first 8 characters of the key (e.g. HKG82W66) in your ticket to support.
         We'll enable the Coupon privilege for this key.
        You must also provide us the IP-addresses from which you will be accessing the API.
        When using this method, there will be no additional confirmations of transactions.
        Please note that you are fully responsible for keeping the secret of the API key safe
            after we have enabled the Withdraw privilege for it.

        :returns
        coupon: Generated coupon.
        transID: Transaction ID.
        funds: Balance after the request.
        """
        parameters = dict(nonce=self._get_nonce(), method="CreateCoupon", currency=currency, amount=amount)
        return self._api_handler.request_trade_api(parameters)

    def redeem_coupon(self, coupon):
        """
        This method is used to redeem coupons.
        Please, note: In order to use this method, you need the Coupon key privilege.
        You can make a request to enable it by submitting a ticket to Support..
        You need to create the API key that you are going to use for this method in advance.
        Please provide the first 8 characters of the key (e.g. HKG82W66) in your ticket to support.
        We'll enable the Coupon privilege for this key.
        You must also provide us the IP-addresses from which you will be accessing the API.
        When using this method, there will be no additional confirmations of transactions.
        Please note that you are fully responsible for keeping the secret of the API key safe
            after we have enabled the Withdraw privilege for it.

        :returns
        couponAmount: The amount that has been redeemed.
        couponCurrency: The currency of the coupon that has been redeemed.
        transID: Transaction ID.
        funds: Balance after the request.
        """
        parameters = dict(nonce=self._get_nonce(), method="RedeemCoupon", coupon=coupon)
        return self._api_handler.request_trade_api(parameters)
