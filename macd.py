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

macd = []
initsts = 1

#*************************＃
#　過去の価格のAVG         ＃
#*************************＃
def AvgCal(statday,cntday):
  cnt = 0
  sum = 0
  while cnt < cntday:
    sum += round(float(price.PriceAction[statday - cnt]['mid']['c']),3)
    cnt += 1
    
  avg =  round(sum / cnt,3)

  return avg
#*************************＃
#　　     MACDのAVG       ＃
#*************************＃
def AvgMacd(macdcnt):
  cnt = 0
  sum = 0
  while cnt < macdcnt:
    sum += round(macd[0]['macd'],3)
    cnt += 1
    
  avg = round(sum / cnt,3)
  return avg
  
#*************************＃
#　　     MACD (TBD)      ＃
#*************************＃
#参考:https://information-station.work/1335/
#26EMA         :EMA
#26本終値の平均:AVG
#現在の価格？  :NOWprice

#AVG+(現在の価格？+AVG) * 2 / (EMA+1)
def MACD():
  
  #初回処理
  if initsts == 1:
    cnt = 0
    while cnt < price.candleCnt:
      np=float(price.PriceAction[price.candleCnt - 1 - cnt]['mid']['c'])
      if cnt < (9 - 1):
        avg9  = 0
        avg12 = 0
        avg26 = 0
      elif cnt == (9 - 1):
        avg9  = AvgCal(price.candleCnt - 1,9)
        avg12 = 0
        avg26 = 0      
      elif cnt < (12 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)#npの改良
        avg12 = 0
        avg26 = 0
      elif cnt == (12 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12  = AvgCal(price.candleCnt - 1,12)
        avg26 = 0
      elif cnt < (26 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12']  ) * 2 / (12 + 1),5)
        avg26 = 0
      elif cnt == (26 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12']  ) * 2 / (12 + 1),5)
        avg26  = AvgCal(price.candleCnt - 1,26)
      else:
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12'] ) * 2 / (12 + 1),5)
        avg26 = round(macd[0]['ema26'] + ( np - macd[0]['ema26'] ) * 2 / (26 + 1),5)
        
      if cnt >= (26 - 1):
        ma = round(avg12 - avg26,8)
      else:
        ma = 0
        
      if cnt == (26 + (9 - 1 - 1)):
        sig = AvgMacd(cnt)
      elif cnt > (26 + (9 - 1 - 1)):
        sig = round(macd[0]['sig'] + ( np - macd[0]['sig'] ) * 2 / (9 + 1),5)
      else:
        sig = 0
            
      macd.insert(0,{"ema9":avg9,"ema12":avg12,"ema26":avg26,"macd":ma,"sig":sig})
      cnt += 1
      
  else:
    np = float(price.getNowPrice())#現在の価格
    macdtime=price.getNowTime()#現在の時間
    if macdtime != nowtime:
      avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),)
      avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12'] ) * 2 / (12 + 1),5)
      avg26 = round(macd[0]['ema26'] + ( np - macd[0]['ema26'] ) * 2 / (26 + 1),5)
      ma = round(avg12 - avg26,5)
      sig = round(macd[0]['sig'] + ( np - macd[0]['sig'] ) * 2 / (9 + 1),5) 
      macd.pop(price.candleCnt - 1)
      macd.insert(0,{"ema9":avg9,"ema12":avg12,"ema26":avg26,"macd":ma,"sig":sig})

      #else時間確定していない場合
      
    
  #return  macd
