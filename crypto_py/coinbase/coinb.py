# https://github.com/coinbase/coinbase-python

import os
from coinbase.wallet.client import Client

client = Client(os.environ['COINKEY'], os.environ['COINSECR'])

#################

client.get_exchange_rates()
client.get_buy_price(currency_pair = 'BTC-USD')
client.get_sell_price(currency_pair = 'BTC-USD')
client.get_spot_price(currency_pair = 'BTC-USD')

#################

user = client.get_current_user()
print(user['name'])

#################

accounts = client.get_accounts()
print(accounts[0])

account = client.get_primary_account()
print(account)

account.get_addresses()
account.get_transactions()
#tx = account.send_money(to='test@test.com', amount='1', currency='BTC', two_factor_token="123456")

client.get_payment_methods()
