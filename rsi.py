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
#　　　　RSI          　　＃
#*************************＃
def RSI(day):

  cnt = 0

  psum = 0
  msum = 0

  while cnt < day:

    A=float(price.PriceAction[(price.candleCnt - 1) - cnt]['mid']['c'])*1000
    B=float(price.PriceAction[((price.candleCnt - 1) - cnt) - 1]['mid']['c'])*1000

    #データが大きいので現在の価格だけ再レスポンスし、最新のデータを取得する。
    #if (day - 1) - cnt == 0:
    #  A = float(price.getNowPrice())*1000

    A = int(A)
    B = int(B)

    zen = A - B
    #print((day - 1) - cnt,":zen:",zen , "( ",A,"-",B, " )")
    if zen > 0:
      psum += zen
    elif zen < 0:
      msum += zen
    cnt += 1
    
  psum  = round(psum,3)
  msum  = round(msum,3)
  #print("puls:",psum,"minus:",msum,"sum",psum + abs(msum))

  #rsi = round(float(psum / (psum + abs(msum)) * 100),2)
  #rsi = round(float(100-(100/(1+((psum/day) / abs(msum/day))))),2)
  rsi = round(float(Fraction(psum/(psum + abs(msum)) * 100)),2)#松井証券の計算式
  
  return rsi