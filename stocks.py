# Predicting Stock Prices in Python
# https://www.youtube.com/watch?v=PuZY9q-aKLw

# Tensorflow couldn't be installed, so the below was used:
# https://github.com/apple/tensorflow_macos
# However, afterwards scikit couldn't be installed
# Finally miniconda was used

import numpy as np
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

company = 'FB'
start = dt.datetime(2012,1,1)
end = dt.datetime(2020,1,1)
data = web.DataReader(company, 'yahoo', start, end)

print("--------------- CLOSE ------------")
print(data['Close'])

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

print("------------ SCALED --------------")
print(scaled_data)

prediction_days = 60

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
  x_train.append(scaled_data[x-prediction_days:x, 0])
  y_train.append(scaled_data[x, 0]) # last day

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) # add one dimension

#x_train.shape: (1857, 60)

print("------- AFTER RESHAPE ---------------------")
print(x_train)

model = Sequential()

#model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
#model.add(Dropout(0.2))
#model.add(LSTM(units=50, return_sequences=True))
#model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)

"""
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
