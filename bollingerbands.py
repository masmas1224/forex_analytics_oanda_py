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
#　　ボリンジャーバントnow  ＃
#*************************＃
def BBprice():
  global PriceAction
  
  # 価格データの取得
  prices = pd.Series([price.PriceAction[price.candleCnt-1-20]['mid']['c'],price.PriceAction[price.candleCnt-1-19]['mid']['c'],price.PriceAction[price.candleCnt-1-18]['mid']['c'], price.PriceAction[price.candleCnt-1-17]['mid']['c'], price.PriceAction[price.candleCnt-1-16 ]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-15]['mid']['c'],price.PriceAction[price.candleCnt-1-14]['mid']['c'],price.PriceAction[price.candleCnt-1-13]['mid']['c'], price.PriceAction[price.candleCnt-1-12]['mid']['c'], price.PriceAction[price.candleCnt-1-11]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-10]['mid']['c'],price.PriceAction[price.candleCnt-1-9]['mid']['c'], price.PriceAction[price.candleCnt-1-8]['mid']['c'],  price.PriceAction[price.candleCnt-1-7]['mid']['c'],  price.PriceAction[price.candleCnt-1-6]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-5]['mid']['c'], price.PriceAction[price.candleCnt-1-4]['mid']['c'], price.PriceAction[price.candleCnt-1-3]['mid']['c'],  price.PriceAction[price.candleCnt-1-2]['mid']['c'],  price.PriceAction[price.candleCnt-1-1]['mid']['c']])
  #print(prices)
  # 移動平均の計算
  window = 20
  rolling_mean = prices.rolling(window).mean()
  #print(rolling_mean)
  # 標準偏差の計算
  rolling_std = prices.rolling(window).std()
  #print(rolling_std)

  # 上下のバンドの計算
  upper_band1 = rolling_mean + 1 * rolling_std
  lower_band1 = rolling_mean - 1 * rolling_std
  upper_band2 = rolling_mean + 2 * rolling_std
  lower_band2 = rolling_mean - 2 * rolling_std
  # 結果の表示
  result = pd.DataFrame({'Price': prices, 'Rolling Mean': rolling_mean, 'Upper Band1': upper_band1, 'Lower Band1': lower_band1, 'Upper Band2': upper_band2, 'Lower Band2': lower_band2})
  return result
#*************************＃
#ボリンジャーバント過去    ＃
#*************************＃
def BBOldprice(i):
  global PriceAction
  
  # 価格データの取得
  prices = pd.Series([price.PriceAction_[price.candleCnt-1-20-i]['mid']['c'],price.PriceAction_[price.candleCnt-1-19-i]['mid']['c'],price.PriceAction_[price.candleCnt-1-18-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-17-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-16-i]['mid']['c'],
                      price.PriceAction_[price.candleCnt-1-15-i]['mid']['c'],price.PriceAction_[price.candleCnt-1-14-i]['mid']['c'],price.PriceAction_[price.candleCnt-1-13-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-12-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-11-i]['mid']['c'],
                      price.PriceAction_[price.candleCnt-1-10-i]['mid']['c'],price.PriceAction_[price.candleCnt-1-9-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-8-i]['mid']['c'],  price.PriceAction_[price.candleCnt-1-7-i]['mid']['c'],  price.PriceAction_[price.candleCnt-1-6-i]['mid']['c'],
                      price.PriceAction_[price.candleCnt-1-5-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-4-i]['mid']['c'], price.PriceAction_[price.candleCnt-1-3-i]['mid']['c'],  price.PriceAction_[price.candleCnt-1-2-i]['mid']['c'],  price.PriceAction_[price.candleCnt-1-1-i]['mid']['c']])
  #print(prices)
  # 移動平均の計算
  window = 20
  rolling_mean = prices.rolling(window).mean()
  #print(rolling_mean)
  # 標準偏差の計算
  rolling_std = prices.rolling(window).std()
  #print(rolling_std)

  # 上下のバンドの計算
  upper_band1 = rolling_mean + 1 * rolling_std
  lower_band1 = rolling_mean - 1 * rolling_std
  upper_band2 = rolling_mean + 2 * rolling_std
  lower_band2 = rolling_mean - 2 * rolling_std
  # 結果の表示
  result = pd.DataFrame({'Price': prices, 'Rolling Mean': rolling_mean, 'Upper Band1': upper_band1, 'Lower Band1': lower_band1, 'Upper Band2': upper_band2, 'Lower Band2': lower_band2})
  return result

#*************************＃
#　　　　　　　　　　　    ＃
#*************************＃
def BBOldprice_(i):
  global PriceAction
  
  # 価格データの取得
  prices = pd.Series([price.PriceAction[price.candleCnt-1-20-i]['mid']['c'],price.PriceAction[price.candleCnt-1-19-i]['mid']['c'],price.PriceAction[price.candleCnt-1-18-i]['mid']['c'], price.PriceAction[price.candleCnt-1-17-i]['mid']['c'], price.PriceAction[price.candleCnt-1-16-i]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-15-i]['mid']['c'],price.PriceAction[price.candleCnt-1-14-i]['mid']['c'],price.PriceAction[price.candleCnt-1-13-i]['mid']['c'], price.PriceAction[price.candleCnt-1-12-i]['mid']['c'], price.PriceAction[price.candleCnt-1-11-i]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-10-i]['mid']['c'],price.PriceAction[price.candleCnt-1-9-i]['mid']['c'], price.PriceAction[price.candleCnt-1-8-i]['mid']['c'],  price.PriceAction[price.candleCnt-1-7-i]['mid']['c'],  price.PriceAction[price.candleCnt-1-6-i]['mid']['c'],
                      price.PriceAction[price.candleCnt-1-5-i]['mid']['c'], price.PriceAction[price.candleCnt-1-4-i]['mid']['c'], price.PriceAction[price.candleCnt-1-3-i]['mid']['c'],  price.PriceAction[price.candleCnt-1-2-i]['mid']['c'],  price.PriceAction[price.candleCnt-1-1-i]['mid']['c']])
  #print(prices)
  # 移動平均の計算
  window = 20
  rolling_mean = prices.rolling(window).mean()
  #print(rolling_mean)
  # 標準偏差の計算
  rolling_std = prices.rolling(window).std()
  #print(rolling_std)

  # 上下のバンドの計算
  upper_band1 = rolling_mean + 1 * rolling_std
  lower_band1 = rolling_mean - 1 * rolling_std
  upper_band2 = rolling_mean + 2 * rolling_std
  lower_band2 = rolling_mean - 2 * rolling_std
  # 結果の表示
  result = pd.DataFrame({'Price': prices, 'Rolling Mean': rolling_mean, 'Upper Band1': upper_band1, 'Lower Band1': lower_band1, 'Upper Band2': upper_band2, 'Lower Band2': lower_band2})
  return result

#*************************＃
#ボリンジャーバント平均幅   ＃
#*************************＃
def BBAverageVolatility():
  
  index = 0
  sum = 0
  while index < 2000:
    price=BBOldprice(index)
    sum += int((round(price['Upper Band2'][19],3)*1000)-(round(price['Lower Band2'][19],3)*1000))

    index += 1
    
  sum = int(sum / 2000)
  Vix = float(sum / 1000)
  Vix = round(Vix,3)
  return Vix
#*************************＃
#ボリンジャーバント幅      ＃
#*************************＃
def BBVolatility():
  BB = BBprice()
  price = int((round(BB['Upper Band2'][19],3)*1000)-(round(BB['Lower Band2'][19],3)*1000))
  price = float(price / 1000)
  price = round(price,3)
  return price