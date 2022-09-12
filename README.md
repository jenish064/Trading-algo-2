# Trading-algo-2

Here I back-tested the the trading strategy based on the following rules of technical indicators.

libraries used:

-talib (for the technical indicators)

-nsepy (for extracting national stock exchange data)

-datetime

-pandas

-numpy

Algorithm-2
-----------

Trading Vehicle and Trade Objective:
Equity Swings

Indicators:
	Market Condition Indicator (to identify the markate trend, range and volatility):
	- Exponential Moving Average-200
	
	Area of value (where might potential buy/sell opportunity come in):
	- Exponential Moving Average-50
	- Stochastic-14


Rules:
	Buying:
	- Exponential Moving Average-50 >= Exponential Moving Average-200(with risk percrntage ema200), AND
	- Latest trading price, above Exponential Moving Average-50(with risk percrntage ema50), AND
	- Stochastic %K line value > Stochastic %D line value, AND
	- Stochastic %K line value >= lowest stochastic point, AND
	- Stochastic %D line value <= lowest stochastic point, AND
	- Demat fund >= Latest trading price

	Selling:
		Strategic:
		- Latest trading price >= (Average purchase price * profitability expectancy rate)
			- Stochastic %K line value < Stochastic %D line value, AND
			- Stochastic %K line value > 70 stochastic point
	OR
		Stop-loss:
		- Latest trading price, below Exponential Moving Average-50(with risk percrntage ema50), OR
		- Exponential Moving Average-50 <= Exponential Moving Average-200(with risk percrntage ema200)
		//- Latest trading price, below by R% of stock purchase value // %R = Risk percentage
	
    Quantity:
    - Decision according to Risk capacity and available fund
