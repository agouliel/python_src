#!./.venv/bin/python

# Predicting Stock Prices in Python
# https://www.youtube.com/watch?v=PuZY9q-aKLw
# https://github.com/apple/tensorflow_macos

import pandas_datareader as web
import datetime as dt
#from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

company = 'FB'
start = dt.datetime(2012,1,1)
end = dt.datetime(2020,1,1)
data = web.DataReader(company, 'yahoo', start, end)
print(data)

"""
sklearn --> MinMaxScaler
tensorflow --> Dense, Dropout, LSTM, Sequential

scaler.fit_transform(data.reshape(-1,1))
x_train --> x-60 : x
y_train --> x (last day)
np.array
np.reshape

Sequential --> add LSTM, Dropout x 3
add Dense
compile('adam', 'mean_squared_error')
fit(epochs=25)

total = concat(data, test)
inputs = total - test - prediction_days
reshape
fit_transform
model.predict
scaler.inverse_transform

plot

real = input + 1 -  prediction_days : input + 1
np.array
np.reshape
model.predict
scaler.inverse_transform
"""
