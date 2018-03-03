import unittest

from wexcon.pair import Pair


class TestPair(unittest.TestCase):
    def setUp(self):
        self.info = {
            "server_time": 1370814956,
            "pairs": {
                "btc_usd": {
                    "decimal_places": 3,
                    "min_price": 0.1,
                    "max_price": 400,
                    "min_amount": 0.01,
                    "hidden": 0,
                    "fee": 0.2
                },
                "btc_eur": {
                    "decimal_places": 3,
                    "min_price": 0.1,
                    "max_price": 400,
                    "min_amount": 0.01,
                    "hidden": 0,
                    "fee": 0.2
                },
                "eur_usd": {
                    "decimal_places": 3,
                    "min_price": 0.1,
                    "max_price": 400,
                    "min_amount": 0.01,
                    "hidden": 0,
                    "fee": 0.2
                }

            }
        }

        self.ticker = {
            "btc_usd": {
                "high": 109.88,
                "low": 91.14,
                "avg": 100.51,
                "vol": 1632898.2249,
                "vol_cur": 16541.51969,
                "last": 101.773,
                "buy": 101.9,
                "sell": 101.773,
                "updated": 1370816308
            },
            "btc_eur": {
                "high": 109.88,
                "low": 91.14,
                "avg": 100.51,
                "vol": 1632898.2249,
                "vol_cur": 16541.51969,
                "last": 101.773,
                "buy": 101.9,
                "sell": 101.773,
                "updated": 1370816308
            },
            "eur_usd": {
                "high": 109.88,
                "low": 91.14,
                "avg": 100.51,
                "vol": 1632898.2249,
                "vol_cur": 16541.51969,
                "last": 101.773,
                "buy": 101.9,
                "sell": 101.773,
                "updated": 1370816308
            }
        }

        self.btc_usd = Pair("btc_usd", self.info, self.ticker)

    def test_getAvailablePairs_checkPairs(self):
        pairs = sorted(self.btc_usd.get_available_pairs(self.info))
        expected_pairs = sorted(["btc_usd", "btc_eur", "eur_usd"])
        self.assertListEqual(expected_pairs, pairs)

    def test_updatePair_checkTicker(self):
        self.btc_usd.update_pair(self.info, self.ticker)
        expected_buy_price = 101.9
        self.assertEqual(expected_buy_price, self.btc_usd.ticker.buy)

    def test_TickerAvgAmount(self):
        self.btc_usd.update_pair(self.info, self.ticker)
        expected_avg_amount = 100.51
        self.assertEqual(expected_avg_amount, self.btc_usd.ticker.avg)

    def test_PublicInfoFeeAmount(self):
        self.btc_usd.update_pair(self.info, self.ticker)
        expected_fee = 0.2
        self.assertEqual(expected_fee, self.btc_usd.info.fee)


if __name__ == "__main__":
    unittest.main()
