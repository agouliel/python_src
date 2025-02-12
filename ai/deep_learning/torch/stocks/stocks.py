#!/Users/agou/miniforge3/envs/tf_env/bin/python
# (or "/usr/bin/env python" if tf_env is active)

# Predicting Stock Prices in Python
# https://www.youtube.com/watch?v=PuZY9q-aKLw

# HELPFUL LINKS:
# https://towardsdatascience.com/installing-tensorflow-on-the-m1-mac-410bb36b776
# https://github.com/apple/tensorflow_macos/issues/153
# https://stackoverflow.com/questions/66060487/valueerror-numpy-ndarray-size-changed-may-indicate-binary-incompatibility-exp
# If the build version used in <1.20, but the installed version is =>1.20, this will lead to an error.
# https://github.com/scikit-learn-contrib/hdbscan/issues/457#issuecomment-773671043
# Whenever those two versions, numpy==* and whatever is pinned, are binary incompatible – as they became suddenly when 1.20.0 got released – this can happen on the user's next build.
# This is also why pinning numpy==1.20.0 will fix it. The installed numpy will be the same as your project builds against. Although, this is only by coincidence for as long as numpy==* continues to be binary compatible. If numpy==1.21.0 got released tomorrow with breaking changes, this would happen again on the next build.

# ACTUAL STEPS:
# 1. Install miniforge
# 2. Download https://raw.githubusercontent.com/mwidjaja1/DSOnMacARM/main/environment.yml
# 3. Change environment.yml to specify numpy 1.19
# 4. conda env create --file=environment.yml --name tf_env
# 5. conda activate tf_env
# 6. pip install --upgrade --force --no-dependencies https://github.com/apple/tensorflow_macos/releases/download/v0.1alpha3/tensorflow_addons_macos-0.1a3-cp38-cp38-macosx_11_0_arm64.whl https://github.com/apple/tensorflow_macos/releases/download/v0.1alpha3/tensorflow_macos-0.1a3-cp38-cp38-macosx_11_0_arm64.whl
# 7. conda install scikit-learn pandas pandas-datareader
# 8. pip install yfinance # pandas-datareader is not working anymore

# WARNINGS:
# tensorflow:AutoGraph could not transform <function Model.make_train_function.<locals>.train_function at 0x12c718040> and will run it as-is.
# Please report this to the TensorFlow team. When filing the bug, set the verbosity to 10 (on Linux, `export AUTOGRAPH_VERBOSITY=10`) and attach the full output.
# Cause: unsupported operand type(s) for -: 'NoneType' and 'int'

# tensorflow:Model was constructed with shape (None, 60, 1) for input
# KerasTensor(type_spec=TensorSpec(shape=(None, 60, 1), dtype=tf.float32, name='lstm_input'), name='lstm_input', description="created by layer 'lstm_input'")
# but it was called on an input with incompatible shape (None, 59, 1).

# ALTERNATIVELY JUST USE PIP:
# pip install tensorflow scikit-learn yfinance

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import yfinance as yf

company = 'AAPL' # FB is delisted

start = '2012-01-01' #dt.datetime(2012,1,1)
end = '2023-01-01'
test_start = end
test_end = '2023-10-01'

#data = web.DataReader(company, 'yahoo', start, end)
data = yf.download(company, start=start, end=end)
print('DOWNLOADED TRAINING DATA')

#print("--------------- CLOSE ------------")
#print(data['Close'])
#2019-12-30    204.410004
#2019-12-31    205.250000

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))

#print("------------ SCALED --------------")
#print(scaled_data)
#[[0.10261801]
# [0.08159383]
# [0.06642639]
# ...
# [0.95294592]
# [0.93447466]
# [0.93867948]]

prediction_days = 60

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
  x_train.append(scaled_data[x-prediction_days:x, 0])
  y_train.append(scaled_data[x, 0]) # last day

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1)) # add one dimension

#x_train.shape: (1857, 60)

#print("------- AFTER RESHAPE ---------------------")
#print(x_train)
#[[[0.10261801]
#  [0.08159383]
#  [0.06642639]
#  ...
#  [0.01641889]
#  [0.02042349]
#  [0.01937228]]

# [[0.8145367 ]
#  [0.81068225]
#  [0.80102117]
#  ...
#  [0.95139407]
#  [0.95294592]
#  [0.93447466]]]

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(x_train, y_train, epochs=25, batch_size=32)
print('FIT ENDED')

test_data = yf.download(company, start=test_start, end=test_end)
print('DOWNLOADED TEST DATA')
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

x_test = []

for x in range(prediction_days, len(model_inputs)):
  x_test.append(model_inputs[x-prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_prices = model.predict(x_test)
print('PREDICT TEST FINISHED')
predicted_prices = scaler.inverse_transform(predicted_prices)

real_data = [model_inputs[len(model_inputs) + 1 - prediction_days:len(model_inputs+1), 0]]

real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))

prediction = model.predict(real_data)
print('PREDICT REAL FINISHED')
prediction = scaler.inverse_transform(prediction)

print('RESULT: ', prediction[0][0])
