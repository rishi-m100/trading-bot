import robin_stocks as r
import sys
import math

lines = open('codes.txt').read().splitlines()
EMAIL = lines[0]
PASSWD = lines[1]
CODE = lines[2]

login = r.robinhood.authentication.login(EMAIL, PASSWD, mfa_code=CODE)

# def QUOTE(ticker):
#     x=r.robinhood.stocks.get_latest_price(ticker)
#     print(ticker.upper() + ": $" + str(x[0]))

    
def BUY_STOCK(ticker, dollars):
    print(f"Buying {dollars} of {ticker}...")
    x = r.robinhood.orders.order_buy_fractional_by_price(ticker, dollars)
    print(x)
    

def SELL_STOCK(ticker, dollars):
    print(f"Selling {dollars} of {ticker}...")
    x = r.robinhood.orders.order_sell_market(ticker, dollars)
    print(x)

def BUY_CRYPTO(ticker, dollars):
    print(f"Buying {dollars} of {ticker}...")
    x = r.robinhood.orders.order_buy_crypto_by_price(ticker, dollars)
    print(x)

def SELL_CRYPTO(ticker, dollars):
    print(f"Selling {dollars} of {ticker}...")
    x = r.robinhood.orders.order_sell_crypto_by_price(ticker,dollars)
    print(x)


TICKER = sys.argv[1:][0].upper()
# QUOTE(TICKER)

if len(sys.argv[1:]) == 3:
    ACTION = sys.argv[1:][1]
    AMOUNT = sys.argv[1:][2]
    AMOUNT = float(AMOUNT)

    if ACTION.upper() == "BUY":
        BUY_STOCK(TICKER, AMOUNT)
    elif ACTION.upper() == "SELL":
        print("Selling " + AMOUNT + " of " + TICKER + "...")
        SELL_STOCK(TICKER, AMOUNT)
elif len(sys.argv[1:]) == 4:
    ACTION = sys.argv[1:][1]
    AMOUNT = sys.argv[1:][2]
    AMOUNT = float(AMOUNT)

    C = sys.argv[1:][3]

    if ACTION.upper() == "BUY":
        if C=="crypto":
            BUY_CRYPTO(TICKER, AMOUNT)
    elif ACTION.upper() == "SELL":
        if C=="crypto":
            SELL_CRYPTO(TICKER, AMOUNT)
#Example Usage:

#python robin.py eth buy 1.0 crypto

#python robin.py aapl buy 1.0

