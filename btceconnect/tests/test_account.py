import unittest

from btceconnect.account import Account


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.get_info_response = {
            "success": 1,
            "return": {
                "funds": {
                    "usd": 325,
                    "btc": 23.998,
                    "ltc": 0,
                },
                "rights": {
                    "info": 1,
                    "trade": 0,
                    "withdraw": 0
                },
                "transaction_count": 15,
                "open_orders": 18,
                "server_time": 1342123547
            }}
        self.account = Account(self.get_info_response)

    def test_update_account_fundsSetup(self):
        usd_funds = self.account.funds.usd
        expected_usd_funds = 325
        self.assertEqual(expected_usd_funds, usd_funds)

    def test_update_account_rightsSetup(self):
        info_right = self.account.rights.info
        expected_info_right = 1
        self.assertEqual(expected_info_right, info_right)

    def test_update_account_openOrdersSetup(self):
        open_orders = self.account.open_orders
        expected_open_orders = 18
        self.assertEqual(expected_open_orders, open_orders)

    def test_update_account_transactionCount(self):
        transactions = self.account.transaction_count
        expected_transactions = 15
        self.assertEqual(expected_transactions, transactions)

    def test_update_account_serverTime(self):
        time = self.account.server_time
        expected_time = 1342123547
        self.assertEqual(expected_time, time)


if __name__ == "__main__":
    unittest.main()
