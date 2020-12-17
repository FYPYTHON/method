# 导入所需的库
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import matplotlib.pyplot as plt

lend_d = 5    # 每个输入数据与前多少个陆续输入的数据有联系
pre_index = 21
layers = 64

# 创建数据框
jdate = ["2020-05-20", "2020-05-21", "2020-05-22", "2020-05-25", "2020-05-26", "2020-05-27", "2020-05-28", "2020-05-29",
         "2020-06-01", "2020-06-02", "2020-06-03", "2020-06-04", "2020-06-05", "2020-06-08", "2020-06-09", "2020-06-10",
         "2020-06-11", "2020-06-12", "2020-06-15", "2020-06-16", "2020-06-17", "2020-06-18"]

jvalue = ["2.7790", "2.8310", "2.7780", "2.8050", "2.8760", "2.8070", "2.7870", "2.8780", "2.9080", "2.8570", "2.8710",
          "2.8780", "2.9100", "2.8650", "2.9150", "2.9840", "2.9780", "3.0360", "3.0860", "3.1580", "3.1960", "3.1150"
          ]

extend_d = ['2020-06-20', '2020-06-21']
extend_v = ['0', '0']
testonly = True
if testonly:
    jdate += extend_d
    jvalue += extend_v

for i in range(len(jvalue)):
    jvalue[i] = float(jvalue[i])
# df = pd.read_csv("data.csv")
df = pd.DataFrame({"Date": jdate, "Close": jvalue})

data = df.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0, len(df)), columns=['Date', 'Close'])
for i in range(0, len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]

# 设置索引
new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)

# 创建训练集和验证集
dataset = new_data.values

train = dataset[0:pre_index, :]
valid = dataset[pre_index:, :]

# 将数据集转换为x_train和y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

x_train, y_train = [], []
for i in range(lend_d, len(train)):
    x_train.append(scaled_data[i - lend_d:i, 0])
    y_train.append(scaled_data[i, 0])
x_train, y_train = np.array(x_train), np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# 创建和拟合LSTM网络
model = Sequential()
model.add(LSTM(units=layers, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=layers))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
# model.compile(loss='mse', optimizer='rmsprop')
model.fit(x_train, y_train, epochs=5, batch_size=1, verbose=2)  # epochs 迭代次数

# 使用过去值来预测246个值
inputs = new_data[len(new_data) - len(valid) - lend_d:].values
inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)

X_test = []
for i in range(lend_d, inputs.shape[0]):
    X_test.append(inputs[i - lend_d:i, 0])
X_test = np.array(X_test)

X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)
print(closing_price)


