"""
Python Project MA 792
Laurie Cuffney
"""

import datetime
import csv
import urllib2
import sys
import scipy
import numpy

from csv import Sniffer
from datetime import datetime
from matplotlib import pylab
from scipy import polyval
from scipy.stats import linregress



"""
This assignement will walk you through gathering data for a
pair of stocks and calculating the correlation between those stocks
using the daily returns.

Yahoo makes their historical stock data available in CSV format.
Below is the url for IBM stock data from Jan 1, 2010 to Dec 31, 2010.
http://ichart.finance.yahoo.com/table.csv?s=IBM&a=00&b=1&c=2010&d=11&e=31&f=2010&g=d&ignore=.csv

The data is returned in CSV (comma separated format) with the flowing columns:
Date, Open, High, Low, Close, Volume, Adj Close

The daily return of
a stock is defined by: 
    (C_n - C_n-1) / C_n-1
where C_n denotes the nth adjusted close and C_n-1 denotes the (n-1)th
adjusted close.

The function signatures for various steps of this process have been
given below. The names and parameters of these functions should not
be changed. You are free to write additional functions or classes as
needed. You are welcome to use any modules in the Python
standard library as well as NumPy, SciPy, and Matplotlib external
libraries. All code must run on Python 2.6.5.
"""

def build_request_url(symbol, start_date, end_date):
    """
    This function should take a stock symbol as a string
    along with the start and end dates as Python dates
    and return the yahoo csv download url.
    """
    
    start_year = start_date.year
    start_month = start_date.month-1
    start_day = start_date.day
    
    end_year = end_date.year
    end_month = end_date.month-1
    end_day = end_date.day
    
    
    url = 'http://ichart.finance.yahoo.com/table.csv?s=%s&a=%d&b=%d&c=%d&d=%d&e=%d&f=%d&g=d&ignore=.csv' %(
            symbol, start_month, start_day, start_year, end_month, end_day,end_year)	
    return url	
	

def get_yahoo_data(url):
    """
    This function should take a url as returned by build_request_url
    and return a list of tuples with each tuple containing the
    date (as a Python date) and the adjusted close (as a float).
    """
    try:
        response = urllib2.urlopen(url, timeout=10)
    except urllib2.HTTPError as e:
        print u'HTTPError getting stock data: %s' % e
        sys.exit(1) 
    except urllib2.URLError as e:
        print u'URLError getting stock data: %s' % e
        sys.exit(1)
    else:
        data_list = []
        reader = csv.reader(response)
        reader.next()
        for row in reader:  
            s = row[0]
            c = row[6]    
            date = datetime.strptime(s,'%Y-%m-%d') 
            adj_close = float(c)
            a = (date,adj_close)
            data_list.append(a)
            
    data_list.reverse()
    return data_list


def calculate_stock_correlation(data):
    """
    This function should take a list containing two lists of the form
    returned by get_yahoo_data (list of date, adj. close tuples) and
    return the correlation of the daily returns as defined above.
    """
    apple_returns = []
    google_returns = []
    
    apple_data = data[0]
    google_data = data[1]
    
    cm = apple_data[0][1]
    
    for i in range(1,len(apple_data)):
        cn = apple_data[i][1]
        daily_return = (cn-cm)/cm
        apple_returns.append(daily_return)
        cm = cn
    
    cm = google_data[0][1]
    
    for i in range(1,len(google_data)):
        cn = google_data[i][1]
        daily_return = (cn-cm)/cm
        google_returns.append(daily_return)
        cm = cn
      
    corr_matrix = scipy.corrcoef(google_returns,apple_returns)
    corr_value = corr_matrix[0][1]  
    return corr_value


def graph_stock_regression(data, filename):
    """
    This function should take a list containing two lists of the form
    returned by get_yahoo_data (list of date, adj. close tuples) and
    save the graph of the series of daily return pairs as well as
    the regression line. The graph should be saved to the given
    filename.
    """
    apple_returns = []
    google_returns = []
    
    apple_data = data[0]
    google_data = data[1]
    
    cm = apple_data[0][1]
    
    for i in range(1,len(apple_data)):
        cn = apple_data[i][1]
        daily_return = (cn-cm)/cm
        apple_returns.append(daily_return)
        cm = cn
    
    cm = google_data[0][1]
    
    for i in range(1,len(google_data)):
        cn = google_data[i][1]
        daily_return = (cn-cm)/cm
        google_returns.append(daily_return)
        cm = cn
        
    (a_s, b_s, r, tt, stderr) = linregress(google_returns, apple_returns)
    line = polyval([a_s, b_s], google_returns)
    pylab.title('Linear Regression')
    pylab.plot(google_returns, apple_returns, 'r.', google_returns, line, 'k')
    pylab.xlabel('Google')
    pylab.ylabel('Apple')
    pylab.legend(['data', 'regression'])
    pylab.savefig(filename)
    


def main():
    """
    This function should get the stock data for Google (GOOG)
    and Apple (AAPL) for Jan 1, 2010 to Dec 31, 2010. Using that
    data it should calculate and print the correlation of the daily
    returns and graph the regression of Google vs Apple. Save the graph as
    GOOGvsAAPL.png
    """
    start = datetime.strptime('2010-01-01','%Y-%m-%d')
    end = datetime.strptime('2010-12-31','%Y-%m-%d')
    
    apple = build_request_url("AAPL", start, end)
    apple_data = get_yahoo_data(apple)
    
    google = build_request_url("GOOG", start, end)
    google_data = get_yahoo_data(google)
    
    data = [apple_data,google_data]
    calculate_stock_correlation(data)
    
    filename = 'GOOGvsAAPL.png'
    graph_stock_regression(data, filename)
	
if __name__ == "__main__":
    """
    When this module as run as a script it will call the main function.
    You should not modify this code.
    """
    main()
