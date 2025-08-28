
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf



# 실현 변동성 
def realized_volatility(x: pd.Series) -> float:
    return np.sqrt((x ** 2).sum())



# AAPL 주식 데이터 받기
df = yf.download(['AAPL'],
                       start='2000-01-01',
                       end='2010-12-31',
                       progress=False, # 진행막대를 표시하지 않는다.
                       auto_adjust=True  # 조정 가격 (기본값)
                       )

df = df.loc[:, ['Close']]
df.rename(columns={'Close': 'adj_close'}, inplace=True)

df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))

df.drop('adj_close', axis=1, inplace=True)
df.dropna(axis=0, inplace=True)


# 월별 실현 변동성
df_rv = df.groupby(pd.Grouper(freq='ME'))['log_rtn'].apply(realized_volatility)
df_rv = df_rv.to_frame(name='rv')


# 값을 연환산
df_rv.rv = df_rv.rv * np.sqrt(12)
print(df_rv)


fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,6))
ax[0].plot(df.index, df.log_rtn, label="Log Return")
ax[0].legend()
ax[1].plot(df_rv.index, df_rv.rv, label="Realized Volatility", color="orange")
ax[1].legend()
plt.show()