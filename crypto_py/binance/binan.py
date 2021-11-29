# https://github.com/binance/binance-connector-python
# pip install binance-connector

from binance.spot import Spot 
import pprint, os

client = Spot()
print(client.time())

client = Spot(key=os.environ['BINKEY'], secret=os.environ['BINSECR'])

# Get account information
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(sorted(client.account()['balances'], key = lambda i: i['asset']))
