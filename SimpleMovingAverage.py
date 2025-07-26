from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts

import time
import pandas as pd
import datetime
from decimal import Decimal
from fractions import Fraction

import price

#*************************＃
#　　 単純移動平均線       ＃
#*************************＃
def AvgPrice(day):
  avg = 0
  sum = 0
  cnt = 0
  while cnt < day:
    A = float(price.PriceAction[(price.candleCnt - 1) - cnt]['mid']['c'])*1000
    A = int(A)
    
    sum += A
    cnt += 1
    
  avg = float((sum / cnt) / 1000)
  avg = round(avg,3)
  
  return avg