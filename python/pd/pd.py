# coding=utf-8
import time
t1 = time.time()
import pandas as pd
import numpy as np
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
if __name__ == "__main__":
    tsp = ts.cumsum()
    print(type(tsp))
    tsp.plot()


