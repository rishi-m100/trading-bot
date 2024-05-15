import schedule
import time
import robin_stocks as r
import os
import sys
import math

# Global variable to store the entry price
entry_price_stock = None
entry_price_crypto = None
count=0
t=0
tick=""
a=0

crypto_action="none"
stock_action="none"

# Function to check the stock price and trigger actions
def check_stock_price(ticker, threshold, action, amount):
    global entry_price_stock
    global count
    global stock_action
    print(stock_action)

    current_price = float(r.robinhood.stocks.get_latest_price(ticker)[0])
    print(f"{ticker} current price: ${current_price}")
    if entry_price_stock is None:
        # Set entry price if it's not set yet
        entry_price_stock = current_price
        print(f"Entry price for {ticker}: ${entry_price_stock}")
    if stock_action == "buy" and current_price <= threshold and count==1:
        count=0
        entry_price_stock = current_price
        print(f"Buying {amount} of {ticker}...")
        os.system(f"python robin.py {ticker} buy {amount}")
        stock_action="sell"
    elif stock_action=="sell" and current_price >= entry_price_stock * 1.1:
        count=1
        # Sell if current price is 10% above entry price
        print(f"{ticker} price exceeds 10% above entry price (${entry_price_stock * 1.1}). Triggering sell action...")
        os.system(f"python robin.py {ticker} sell {amount}")
        entry_price_stock = None  # Reset entry price after selling
        stock_action="buy"

def check_crypto_price(ticker, threshold, action, amount):
    global entry_price_crypto
    global count
    global crypto_action
    global t
    print(crypto_action)

    current_price = float(r.robinhood.crypto.get_crypto_quote(ticker)["ask_price"])
    print(f"{ticker} current price: ${current_price}")
    if entry_price_crypto is None:
        # Set entry price if it's not set yet
        entry_price_crypto = current_price
        print(f"Entry price for {ticker}: ${entry_price_crypto}")
    if crypto_action== "buy" and current_price < threshold and count==1:
        count=0
        entry_price_crypto = current_price
        print(f"Buying {amount} of {ticker}...")

        ##
        # print(f"python robin.py {ticker} buy {amount} crypto")
        os.system(f"python robin.py {ticker} buy {amount} crypto")
        crypto_action="sell"
    elif crypto_action=="sell" and current_price >= entry_price_crypto * 1.10:
        count=1
        # Sell if current price is 5% above entry price
        print(f"{ticker} price exceeds 10% above entry price (${entry_price_crypto * 1.10}). Triggering sell action...")
        os.system(f"python robin.py {ticker} sell {amount} crypto")
        entry_price_crypto = None  # Reset entry price after selling
        crypto_action="buy"
        t=current_price


# Function to schedule the job for checking stock prices
def schedule_stock_check():
    global count
    global stock_action
    global t
    global tick
    global a
    # Define your monitoring parameters here
    ticker = tick  # Change this to the stock ticker you want to monitor
    threshold = float(t)  # Change this to your desired buy threshold
    sell_threshold = None  # No need for sell threshold here
    # action = sys.argv[1:][1]  # Change this to "buy" or "sell" based on your requirement
    amount = a   # Change this to the amount you want to buy/sell
    # Schedule the job to run every 30 seconds
    if stock_action=="buy":
            count+=1
    schedule.every(1).seconds.do(check_stock_price, ticker, threshold, stock_action, amount)

def schedule_crypto_check():
    global count
    global crypto_action
    global t
    global tick
    global a
    # Define your monitoring parameters here
    ticker = tick  # Change this to the stock ticker you want to monitor
    threshold = float(t) # Change this to your desired buy threshold
    sell_threshold = None  # No need for sell threshold here
    amount = a

    if crypto_action=="buy":
            count+=1
    # amount = round(amount, 1)
       # Change this to the amount you want to buy/sell
    # Schedule the job to run every 30 seconds
    schedule.every(4).seconds.do(check_crypto_price, ticker, threshold, crypto_action, amount)

# Main function to start the monitoring process
def main():
    global crypto_action
    global stock_action
    global t
    global tick
    global a

    # Login to Robinhood
    lines = open('codes.txt').read().splitlines()
    EMAIL = lines[0]
    PASSWD = lines[1]
    CODE = lines[2]
    r.robinhood.authentication.login(EMAIL, PASSWD, mfa_code=CODE)

    asset_type = input("Asset Type (stock/crypto): ")

    # asset_type = sys.argv[1:][0]
       # Change this to "buy" or "sell" based on your requirement

    # Schedule the stock check job
    if asset_type=='stock':
        tick = input("Ticker: ")
        tick = tick.upper()
        stock_action = input("Action (buy/sell): ")
        a = input("Amount: ")
        if stock_action=="buy":
            t= input("Min threshold price: ")
        schedule_stock_check()
    elif asset_type=='crypto':
        # crypto_action = sys.argv[1:][1]
        tick = input("Ticker: ")
        tick = tick.upper()
        crypto_action = input("Action (buy/sell): ")
        a = input("Amount: ")
        if crypto_action=="buy":
            t= input("Min threshold price: ")
        schedule_crypto_check()
    
        # Run the scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
    

if __name__ == "__main__":
    main()

#Example Usage:
#python scheduler.py 
