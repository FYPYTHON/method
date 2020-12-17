# coding=utf-8
import time
t1 = time.time()
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("import used", time.time() - t1)
ts = pd.Series(np.random.randn(100), index=pd.date_range('12/12/2019', periods=100))

dates = pd.date_range('20130101', periods=6)
print(dates)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))

print(df)

print(df.loc['20130102':'20130104', ['A', 'B']])
print(df.iloc[0:3, 2:3])
print(df.at[dates[0], 'B'])
# int index
print(df.iloc[1, 2])
print(df.iat[1, 2])
# df.groupby("A").sum()
print("used time:", time.time() - t1)
# df.cumsum().plot()
# save to csv
# df.to_csv("df.csv")
# df = pd.read_csv("df.csv")
# df.to_excel('foo.xlsx', sheet_name='Sheet1')
a1 = df[df['A'].isin([0.5, 0.1])]
a2 = df[(df['A'] > 0.5) | (df['B'] < 0.1)]    # () must
a_notna = df[df['C'].notna()]
a4 = df.loc[df['A'] > 0.7, "C"]
a5 = df.iloc[1:3, 3:5]
print(df.head(3))    # first 3
print(df.tail(3))    # last 3
print("a1:", a1)
print("a2:", a2)
print("a4:", a4)
print("a5:", a5)

print(a_notna.shape)
c1 = df.agg({"C": ['min', 'max', 'median', 'skew']})
print(c1)
if __name__ == "__main__":
    pass
    # tsp = ts.cumsum()
    # print(type(tsp))
    # tsp.plot()



