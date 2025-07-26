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

import STRUCT as St

st=St.STRUCT()

accountID = st.accountID
access_token = st.access_token

candleCnt = st.candleCnt
global PriceAction
global PriceAction_
#*************************＃
#　　過去の価格を取得する。 ＃
#*************************＃
def getOldCandlesClole_(cnt,gran):
  try:
    global PriceAction_

    params = {
      "count": cnt,
      "granularity": gran
    }
    api = API(access_token=access_token, environment="practice")
    r = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
    PriceAction_ = api.request(r)['candles']
  except ZeroDivisionError:
    print("streaming error")

#*************************＃
#　　過去の価格を取得する。 ＃
#*************************＃
def getOldCandlesClole(cnt,gran):
  try:
    global PriceAction

    params = {
      "count": cnt,
      "granularity": gran
    }
    api = API(access_token=access_token, environment="practice")
    r = instruments.InstrumentsCandles(instrument="USD_JPY", params=params)
    PriceAction = api.request(r)['candles']
  except ZeroDivisionError:
    print("streaming error")

#*************************＃
#　　現在の価格を取得する。 ＃
#*************************＃
def getNowPrice():
  return PriceAction[candleCnt - 1]['mid']['c']

#*************************＃
#　　現在の時間を取得する。 ＃
#*************************＃
def getNowTime():
  return PriceAction[0]['time']

#*************************＃
#　   　  注文処理         ＃
#*************************＃
def OrderExchange(units,instrument):
  try:
    data = {
      "order": {
        "units": units,
        "instrument": instrument,
        "timeInForce": "FOK",
        "type": "MARKET",
        "positionFill": "DEFAULT"
      }
    }
    api = API(access_token=access_token, environment="practice")
    r = orders.OrderCreate(accountID, data=data)
    get=api.request(r)
  except ZeroDivisionError:
    print("streaming error")
    
  return get
  
#*************************＃
#　 ポジション解消処理(TBD)＃
#*************************＃
def PositionTermination():
  try:
    data = {
      "order": {
        "timeInForce": "GTC",
        "price": "147.33",
        "type": "MARKET",
        "tradeID": "24"
      }
    }
    api = API(access_token=access_token, environment="practice")
    r = orders.OrderCreate(accountID, data=data)
    get=api.request(r)
  except ZeroDivisionError:
    print("streaming error")