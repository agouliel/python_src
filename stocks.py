#!/Users/agou//python_virtual_env/stocks_env/bin/python

# https://www.youtube.com/watch?v=PuZY9q-aKLw

import pandas_datareader as web
import datetime as dt

company = 'FB'
start = dt.datetime(2012,1,1)
end = dt.datetime(2020,1,1)
data = web.DataReader(company, 'yahoo', start, end)
print(data)
