import sys
import os
from fredapi import Fred
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../'))  
sys.path.append(project_root) 

from utils.get_key import FRED_API_KEY

def get_fred_cpi():

    # API 키 발급: https://fred.stlouisfed.org/
    fred = Fred(api_key=FRED_API_KEY)

    # 미국 CPI 지수 (CPIAUCSL: Consumer Price Index for All Urban Consumers)
    return fred.get_series("CPIAUCSL")
