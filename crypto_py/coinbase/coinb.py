# https://github.com/coinbase/coinbase-python

import os
from coinbase.wallet.client import Client

client = Client(os.environ['COINKEY'], os.environ['COINSECR'])

user = client.get_current_user()
print(user['name'])
print(user['email'])

#balance = coinbase.get_balance()
#print('Balance is ' + balance)
