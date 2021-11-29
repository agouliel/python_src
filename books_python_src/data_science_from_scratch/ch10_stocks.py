import datetime
from collections import namedtuple, defaultdict
#from typing import NamedTuple

StockPrice = namedtuple('StockPrice', ['symbol', 'date', 'closing_price'])

data = [
  StockPrice('MSFT', datetime.date(2018, 12, 26), 108.03),
  StockPrice('MSFT', datetime.date(2018, 12, 25), 107.03),
  StockPrice('MSFT', datetime.date(2018, 12, 24), 106.03),

  StockPrice('AAPL', datetime.date(2018, 12, 24), 109.03),
  StockPrice('AAPL', datetime.date(2018, 12, 25), 110.03),
  StockPrice('AAPL', datetime.date(2018, 12, 26), 111.03),
]

prices = defaultdict(list)

for sp in data:
  prices[sp.symbol].append(sp)

prices = {symbol: sorted(StockPrice_list) for symbol, StockPrice_list in prices.items()}

def pct_change(yesterday, today):
  return today.closing_price / yesterday.closing_price - 1

DailyChange = namedtuple('DailyChange', ['symbol', 'date', 'pct_change'])

def day_over_day_changes(prices):
  return [DailyChange(today.symbol, today.date, pct_change(yesterday, today))
          for yesterday, today in zip(prices, prices[1:])]

all_changes = [change
               for StockPrice_list in prices.values()
               for change in day_over_day_changes(StockPrice_list)]

print(all_changes)

# [
# DailyChange(symbol='MSFT', date=datetime.date(2018, 12, 25), pct_change=0.009431293030274457), 
# DailyChange(symbol='MSFT', date=datetime.date(2018, 12, 26), pct_change=0.009343174810800603),
 
# DailyChange(symbol='AAPL', date=datetime.date(2018, 12, 25), pct_change=0.009171787581399693), 
# DailyChange(symbol='AAPL', date=datetime.date(2018, 12, 26), pct_change=0.009088430428065175)
# ]
