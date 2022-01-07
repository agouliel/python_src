# https://www.youtube.com/watch?v=4KsP5Et_aWo
# https://github.com/Sven-Bo/portfolio-tracking-excel-python
# https://docs.xlwings.org/en/stable/installation.html
# https://stackoverflow.com/questions/67962353/please-help-me-run-a-python-script-from-excel-365-vba-on-a-mac-mini-running-big
# /Users/agou/Library/Application Scripts/com.microsoft.Excel

from enum import Enum
import time, os, sys
import xlwings as xw
import pandas as pd
from yahoofinancials import YahooFinancials  # pip install yahoofinancials

class Column(Enum):
    long_name = 1
    current_price = 5
    currency = 6

def pull_stock_data(tickers):
    if tickers:
        print(f"Iterating over the following tickers: {tickers}")
        df = pd.DataFrame()
        for ticker in tickers:
            data = YahooFinancials(ticker)
            open_price = data.get_open_price()

            # If no open price can be found, Yahoo Finance will return 'None'
            if open_price is None:
                # If opening price is None, append empty dataframe (row)
                print(f"Ticker: {ticker} not found on Yahoo Finance. Please check")
                df = df.append(pd.Series(dtype=str), ignore_index=True)
            else:
                try:
                    try:
                        long_name = data.get_stock_quote_type_data()[ticker]["longName"]
                    except (TypeError, KeyError):
                        long_name = None

                    ticker_currency = data.get_currency()

                    new_row = {
                        "currency": ticker_currency,
                        "long_name": long_name,
                        "current_price": data.get_current_price(),
                    }
                    df = df.append(new_row, ignore_index=True)
                    print(f"Successfully pulled financial data for: {ticker}")

                except Exception as e:
                    # Error Handling
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    # Append Empty Row
                    df = df.append(pd.Series(dtype=str), ignore_index=True)
        return df
    return pd.DataFrame()

def main():
  wb = xw.Book.caller()

  #wb.sheets[0].range('A1').value = 'Hello World!'
  #df = wb.sheets[0].range('A1').options(pd.DataFrame).value

  mylist = wb.sheets[0].range('A1').expand('down').value # expand-down gets the whole column

  #wb.sheets[0].range('B1').value = [[item] for item in mylist] # column orientation
  #wb.sheets[0].range('B1').value = mylist # row orientation

  df = pull_stock_data(mylist)
  wb.sheets[0].range('B1').options(index=False, header=False).value = df
