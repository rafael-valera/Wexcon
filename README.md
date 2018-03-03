Python API to connect to your WEX account through the WEX API and structure your account information
so you can focus only developing your trading stragegy.

It's purely written in Python3, no external libraries required.

Installation:

    pip install git+https://github.com/rafael-valera/wexcon

Usage:

    import wexcon

Create a Trader object to query de WEX public and trade API

    trader = wexcon.Trader(KEY, SECRET)

Create a Account object to initialize your account information (funds, rights, transaction count, etc)

    get_info = trader.get_info()
    my_account = wexcon.Account(get_info_response=get_info)

    usd_balance = my_account.funds.usd
    trade_right = my_account.rights.trade
    open_orders = my_account.info.open_orders

Update your account the same way it was created:

    get_info = trader.get_info()
    my_account.update_account(get_info_response=get_info)


Create a Pair object to play your game:

    public_info = trader.puclic_info()
    ticker_info = trader.ticker_public()

    btc_usd = wexcon.Pair(pair_name=wexcon.BTCUSD, public_info_response=public_info, ticker_response=ticker_info)

    btc_usd_fee = btc_usd.info.fee
    btc_usd_decimal_places = btc_usd.info.decimal_places

    btc_usd_buy_price = btc_usd.ticker.buy
    btc_usd_buy_avg = btc_usd.ticker.avg

    using the static method get_available_pairs(public_info) you can retrieve a list of the current available pairs

Update the trading Pair object:

    public_info = trader.public_info()
    ticker_info = trader.ticker_public()

    btc_usd.update_pair(public_info, ticker_info)


Ticker GUI

    You can download/clone the repo
    Open the script ticker_gui_application.py with your favorite editor
    Place your API key/secret in main() function and run it.


Please feel free to let me know what you think... It would be a lot of help!





