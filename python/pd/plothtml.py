# coding=utf-8
import base64
from io import BytesIO
from pandas import Series
from numpy.random import randint
import matplotlib.pyplot as plt

s = Series(randint(1, 10, 20))
print(s)
print(s.cumsum())
plt.plot(s.cumsum())
imgbuff = BytesIO()
plt.savefig(imgbuff)
imgdata = imgbuff.getvalue()
# print(imgdata)
imbase64 = base64.b64encode(imgdata)
ims = imbase64.decode()
imd = "data:image/png;base64,"+ims
print("-"*20)
# print(imd)
print(len(imd))
print(type(imd))
# plt.show()