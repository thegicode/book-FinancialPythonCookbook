import sys
import os
import numpy as np
import pandas as pd
import yfinance as yf

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  
sys.path.append(project_root) 

from utils.fred_cpi import get_fred_cpi

# AAPL 주식 데이터 받기
df = yf.download(['AAPL'],
                       start='2000-01-01',
                       end='2010-12-31',
                       progress=False, # 진행막대를 표시하지 않는다.
                    #    actions='inline', # 배당이나 액면분할
                       auto_adjust=True  # 조정 가격 (기본값)
                       )

# print(df)

# df = df.loc[:, ['Close']]
# df.rename(columns={'Close': 'adj_close'}, inplace=True)

# 단순 수익률, 로그 수익률 계산
# df['simple_rtn'] = df.adj_close.pct_change()
# df['log_rtn'] = np.log(df.adj_close/df.adj_close.shift(1))
# print(df)

# AAPL 월말 종가 (단일 시리즈 → DataFrame)
adj_close_m = df['Close']['AAPL'].rename('adj_close').resample('ME').last().to_frame()

# 2) CPI (월간)
cpi = get_fred_cpi().rename("cpi")
cpi = cpi.loc["2000-01-01":"2010-12-31"]
cpi_m = cpi.resample('ME').last().rename('cpi').to_frame()

#  병합 
df_merged = adj_close_m.join(cpi_m, how='inner')

# 단순수익률과 인플레이션 계산
df_merged['simple_rtn'] =  df_merged.adj_close.pct_change()
df_merged['inflation_rate'] =  df_merged.cpi.pct_change()

# 인플레이션에 따른 수익률을 조정
df_merged['real_rtn'] = (df_merged.simple_rtn + 1) / (df_merged.inflation_rate + 1) - 1

print(df_merged)



