Gathers data for a pair of stocks and calculates the correlation between those stocks
using the daily returns.

Data used was pulled from Yahoo historical stock data.
Below is the url for IBM stock data from Jan 1, 2010 to Dec 31, 2010.
http://ichart.finance.yahoo.com/table.csv?s=IBM&a=00&b=1&c=2010&d=11&e=31&f=2010&g=d&ignore=.csv
The data is returned in CSV (comma separated format) with the flowing columns:
Date, Open, High, Low, Close, Volume, Adj Close

The daily return of
a stock is defined by: 
    (C_n - C_n-1) / C_n-1
where C_n denotes the nth adjusted close and C_n-1 denotes the (n-1)th
adjusted close.

All code runs on Python 2.6.5.
