# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/danielsmithdevelopment/python-group-programming/blob/python-for-finance/portfolio_optimization_intro.ipynb
"""

# Description: Program attempts to optimize a user's portfolio using Efficient Frontier

# pip3 install PyPortfolioOpt

# Import libraries
from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Get stock symbols/tickers in portfolio
assets = ['SPYG', 'QQQ', 'VYMI', 'SLV', 'GLD', 'ARKK', 'ARKF', 'ARKQ']

# Get the stock/portfolio starting date
stockStartDate = '2020-01-01'

# Get the stock/portfolio ending date
today = datetime.today().strftime('%Y-%m-%d')

# Create a dataframe to store the adjusted close price of stocks
df = pd.DataFrame()

# Store the adjusted close price of the stock into the dataframe
for stock in assets:
  df[stock] = web.DataReader(stock, data_source='yahoo', start = stockStartDate, end = today)['Adj Close']

# Show dataframe
df

# Show the daily simple return
returns = df.pct_change()
returns

# Visually show the stock/portfolio
title = 'Portfolio Adj. Close Price History'

# Get the stocks
my_stocks = df
# my_stocks = returns

# Create and plot the graph
for c in my_stocks.columns.values:
  plt.plot(my_stocks[c], label = c)

plt.title(title)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Adj. Close Price ($)', fontsize = 18)
plt.yscale("log")
plt.legend(my_stocks.columns.values, loc='upper left')
plt.rcParams["figure.figsize"] = (15,10)
plt.show()

# Create and show the annualized covariance matrix
cov_matrix_annual = returns.cov() * 252
cov_matrix_annual

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Portfolio Optimization

# Calculate the expected returns and annualized sample covariance matrix of asset returns
mu = expected_returns.mean_historical_return(df, compounding=True)
S = risk_models.sample_cov(df)

# Optimize for maximum Sharpe Ratio
ef = EfficientFrontier(mu, S, weight_bounds=(0.05,0.2))
# weights = ef.max_sharpe(risk_free_rate=0.01)
weights = ef.min_volatility()
ef.save_weights_to_file('weights.csv')
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose = True)

# Get the discrete allocation of each share per stock
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = 15000)

allocation, leftover = da.lp_portfolio()
print('Discrete allocation:', allocation)
print('Funds remaining: ${:.2f}'.format(leftover))