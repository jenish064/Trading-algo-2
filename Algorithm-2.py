transactions = 0
first_buy = True
first_buy_str = []


import talib
from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np


# important variables for indicators
START_DATE = date(2018, 3, 10)
END_DATE = date.today()
STOCH_INTERVAL_DAYS = 14
STOCH_LOWER_BAND = 40
STOCH_HIGHER_BAND = 70

# date list to traverse through the dictionary
try:
    date_list = [str(date) for date in get_history(symbol="SBIN", start=START_DATE, end=END_DATE).index]
except AttributeError:
    print("AttributeError1 while fetching data for date_list, wait a while...")
    try:
        date_list = [str(date) for date in get_history(symbol="SBIN", start=START_DATE, end=END_DATE).index]
    except AttributeError:
        print("AttributeError2 while fetching data for date_list, wait a while...")
        try:
            date_list = [str(date) for date in get_history(symbol="SBIN", start=START_DATE, end=END_DATE).index]
        except AttributeError:
            print("AttributeError3 while fetching data for date_list, wait a while...")
# gathering NSE top100 ticker's list
ticker_list = pd.read_csv("nifty50_csv.csv")['Symbol'].to_list() #pd.read_csv("top100 NSE_csv.csv")['Symbol'].to_list()

# portfolio Variables
portfolio = {ticker: {"quantity": 0, "average_trading_price": 0, "PNL": [], "Profit_fulfillment_bool_trigger": False} for ticker in ticker_list}


INITIAL_AMOUNT = 10000
demat_fund = 10000
invested_amount = 0
PROFITABILITY_EXPECTANCY_RATE = 1.05
risk_ema50 = 5
risk_ema200 = 10


# raw data for each ticker
try:
    raw_data_nse100 = {ticker: get_history(ticker, START_DATE, END_DATE) for ticker in ticker_list}
except AttributeError:
    print("AttributeError1 while fetching data for raw_data_nse100, wait a while...")
    try:
        raw_data_nse100 = {ticker: get_history(ticker, START_DATE, END_DATE) for ticker in ticker_list}
    except AttributeError:
        print("AttributeError2 while fetching data for raw_data_nse100, wait a while...")
        try:
            raw_data_nse100 = {ticker: get_history(ticker, START_DATE, END_DATE) for ticker in ticker_list}
        except AttributeError:
            print("AttributeError3 while fetching data for raw_data_nse100, wait a while...")

# indicators
#ema50 for every ticker
ema50_nse100 = {}
for ticker in ticker_list:
    try:
        ema50_nse100[ticker] = talib.EMA(raw_data_nse100[ticker]['Close'], 50)
    except:
        print('Error EMA 50, fetching data for', ticker)

#ema200 for every ticker
ema200_nse100 = {}
for ticker in ticker_list:
    try:
        ema200_nse100[ticker] = talib.EMA(raw_data_nse100[ticker]['Close'], 200)
    except:
        print('Error EMA 200, fetching data for', ticker)

#stochastic for every ticker
stoch14_nse100 = {}
for ticker in ticker_list:
    try:
        stoch14_nse100[ticker] = talib.STOCH(raw_data_nse100[ticker]['High'], raw_data_nse100[ticker]['Low'], raw_data_nse100[ticker]['Close'], 14)
    except:
        print('Error STOCH 14, fetching data for', ticker)


needed_fund = 0
# strategy excecution
for date_index in range(0, len(date_list)-1):
    for ticker in ticker_list:
        try:
            current_ticker_price = np.round(raw_data_nse100[ticker]["Close"][date_index], 2)
            current_ticker_ema200 = np.round(ema200_nse100[ticker][date_index], 2)
            current_ticker_ema50 = np.round(ema50_nse100[ticker][date_index], 2)
            current_ticker_stoch_K = np.round(stoch14_nse100[ticker][0][date_index], 2)
            current_ticker_stoch_D = np.round(stoch14_nse100[ticker][1][date_index], 2)


            #buy rules syntax
            if (current_ticker_ema50 >= (current_ticker_ema200 * (1-(risk_ema200/100)))) and (current_ticker_price > (current_ticker_ema50 * (1-(risk_ema50/100)))) and ((current_ticker_stoch_K > current_ticker_stoch_D) and (current_ticker_stoch_K >= STOCH_LOWER_BAND) and (current_ticker_stoch_D <= STOCH_LOWER_BAND)):
                
                if demat_fund >= current_ticker_price:
                    
                    #first buy
                    if first_buy:
                        first_buy = False
                        first_buy_str = [date_list[date_index]," BUY -- ", ticker, " Price: ",current_ticker_price, "ema200: ", current_ticker_ema200, "ema50: ",current_ticker_ema50, " %K: ", current_ticker_stoch_K, " %D: ", current_ticker_stoch_D, "\n Demat fund: ", demat_fund, "    current ", ticker, "quantity: ", portfolio[ticker]["quantity"]]
                        
                    demat_fund -= current_ticker_price
                    portfolio[ticker]["average_trading_price"] = (((portfolio[ticker]["average_trading_price"] * portfolio[ticker]["quantity"]) + current_ticker_price) / (portfolio[ticker]["quantity"] + 1))
                    portfolio[ticker]["quantity"] = portfolio[ticker]["quantity"] + 1
                    portfolio[ticker]["PNL"].append((date_list[date_index], "BOUGHT for", current_ticker_price, portfolio[ticker]["average_trading_price"], portfolio[ticker]["quantity"]))
                                                  
                    print(date_list[date_index]," BUY -- ", ticker, " Price: ",current_ticker_price, " ema200: ",current_ticker_ema200, " ema50: ",current_ticker_ema50, " %K: ", current_ticker_stoch_K, " %D: ", current_ticker_stoch_D, "\n Demat fund: ", demat_fund, "    current ", ticker, "quantity: ", portfolio[ticker]["quantity"], " average price: ", portfolio[ticker]["average_trading_price"])
    
                    transactions += 1
                    
                elif demat_fund < current_ticker_price:
                    needed_fund += current_ticker_price - demat_fund
                    demat_fund += current_ticker_price - demat_fund
                    
                    demat_fund -= current_ticker_price
                    portfolio[ticker]["average_trading_price"] = (((portfolio[ticker]["average_trading_price"] * portfolio[ticker]["quantity"]) + current_ticker_price) / (portfolio[ticker]["quantity"] + 1))
                    portfolio[ticker]["quantity"] = portfolio[ticker]["quantity"] + 1
                    portfolio[ticker]["PNL"].append((date_list[date_index], "BOUGHT for", current_ticker_price, portfolio[ticker]["average_trading_price"], portfolio[ticker]["quantity"]))
                                                  
                    print(date_list[date_index]," BUY -- ", ticker, " Price: ",current_ticker_price, " ema200: ",current_ticker_ema200, " ema50: ",current_ticker_ema50, " %K: ", current_ticker_stoch_K, " %D: ", current_ticker_stoch_D, "\n Demat fund: ", demat_fund, "    current ", ticker, "quantity: ", portfolio[ticker]["quantity"], " average price: ", portfolio[ticker]["average_trading_price"])
    
                    transactions += 1

            #sell rules syntax
            if portfolio[ticker]["quantity"] > 0:
                
                if current_ticker_price >= (portfolio[ticker]["average_trading_price"] * PROFITABILITY_EXPECTANCY_RATE):
                    portfolio[ticker]["Profit_fulfillment_bool_trigger"] = True

                if current_ticker_price < (current_ticker_ema50 * (1-(risk_ema50/100))):

                    demat_fund += current_ticker_price * portfolio[ticker]["quantity"]
                    portfolio[ticker]["PNL"].append((date_list[date_index], "SOLD for", current_ticker_price, portfolio[ticker]["average_trading_price"], "PNL: ",
                                          ((current_ticker_price - portfolio[ticker]["average_trading_price"]) * 100) / portfolio[ticker]["average_trading_price"]))
                    portfolio[ticker]["quantity"] = 0
                    portfolio[ticker]["average_trading_price"] = 0

                    print(date_list[date_index]," SELL -- ", ticker, " Price: ",current_ticker_price, " ema200: ",current_ticker_ema200, " ema50: ",current_ticker_ema50, " %K: ", current_ticker_stoch_K, " %D: ", current_ticker_stoch_D, "\n Demat fund: ", demat_fund, "    current ", ticker, "quantity: ", portfolio[ticker]["quantity"], " average price: ", portfolio[ticker]["average_trading_price"], "REASON: Hit below EMA-200")
                    
                    transactions += 1


                if (current_ticker_stoch_K < STOCH_HIGHER_BAND) and (current_ticker_stoch_K < current_ticker_stoch_D) and (current_ticker_stoch_D >= STOCH_HIGHER_BAND) and (portfolio[ticker]["Profit_fulfillment_bool_trigger"] == True):

                    demat_fund += current_ticker_price * portfolio[ticker]["quantity"]
                    portfolio[ticker]["PNL"].append((date_list[date_index], "SOLD for", current_ticker_price, portfolio[ticker]["average_trading_price"], "PNL: ",
                                          ((current_ticker_price - portfolio[ticker]["average_trading_price"]) * 100) / portfolio[ticker]["average_trading_price"]))
                    portfolio[ticker]["quantity"] = 0
                    portfolio[ticker]["average_trading_price"] = 0
                    portfolio[ticker]["Profit_fulfillment_bool_trigger"] = False

                    print(date_list[date_index]," SELL ", ticker, " Price: ",current_ticker_price, " ema200: ",current_ticker_ema200, " ema50: ",current_ticker_ema50, " %K: ", current_ticker_stoch_K, " %D: ", current_ticker_stoch_D, "\n Demat fund: ", demat_fund, "    current ", ticker, "quantity: ", portfolio[ticker]["quantity"], " average price: ", portfolio[ticker]["average_trading_price"], "REASON: Selling by Stochastic indication")
                    
                    transactions += 1

        except IndexError:    # 'IndexError' is likely to happen, so to avoid that exception handling is used
            print("IndexError in ", ticker)
        except KeyError:
            print("KeyError in ", ticker)
            

for ticker in portfolio.keys():    # Counting total invested amount by multiplying the current portfolio ticker quantity with the current respective price
    try:    # 'IndexError' exception handling
        current_ticker_price = get_history(symbol=ticker, start=START_DATE, end=END_DATE)['Close'][-3]
        invested_amount += current_ticker_price * portfolio[ticker]["quantity"]
        
    except AttributeError:
        print("portfolio counting AttributeError1 in", ticker)
        try:    # 'IndexError' exception handling
            current_ticker_price = get_history(symbol=ticker, start=START_DATE, end=END_DATE)['Close'][-3]
            invested_amount += current_ticker_price * portfolio[ticker]["quantity"]
        except AttributeError:
            print("portfolio counting AttributeError2 in", ticker)
            try:    # 'IndexError' exception handling
                current_ticker_price = get_history(symbol=ticker, start=START_DATE, end=END_DATE)['Close'][-3]
                invested_amount += current_ticker_price * portfolio[ticker]["quantity"]
            except AttributeError:
                print("portfolio counting AttributeError3 in", ticker)

    except IndexError:
        print("portfolio counting IndexError in", ticker)

    except KeyError:
        print("portfolio counting KeyError in  ", ticker)

print("Demat Fund: ", demat_fund, "\n",
      "Invested Fund's Current Value: ", invested_amount, "\n",
      "Total Profit: ", np.round((invested_amount+demat_fund-INITIAL_AMOUNT) * 100 / INITIAL_AMOUNT, 2), "%")

print(needed_fund + 10000)