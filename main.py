

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

candleCnt = 200

macd = []
global PriceAction
initsts = 1
nowtime = ""

macdtime = ""

accountID = ""
access_token = ''

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

  
#*************************＃
#　　現在の価格を取得する。 ＃
#*************************＃
def getNowPrice():
  return PriceAction[candleCnt - 1]['mid']['c']


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
#　　現在の時間を取得する。 ＃
#*************************＃
def getNowTime():
  return PriceAction[0]['time']

#*************************＃
#　　ボリンジャーバント     ＃
#*************************＃
def BollingerBands():
  global PriceAction
  
  # 価格データの取得
  prices = pd.Series([PriceAction[candleCnt-1-20]['mid']['c'],PriceAction[candleCnt-1-19]['mid']['c'],PriceAction[candleCnt-1-18]['mid']['c'], PriceAction[candleCnt-1-17]['mid']['c'], PriceAction[candleCnt-1-16 ]['mid']['c'],
                      PriceAction[candleCnt-1-15]['mid']['c'],PriceAction[candleCnt-1-14]['mid']['c'],PriceAction[candleCnt-1-13]['mid']['c'], PriceAction[candleCnt-1-12]['mid']['c'], PriceAction[candleCnt-1-11]['mid']['c'],
                      PriceAction[candleCnt-1-10]['mid']['c'],PriceAction[candleCnt-1-9]['mid']['c'], PriceAction[candleCnt-1-8]['mid']['c'],  PriceAction[candleCnt-1-7]['mid']['c'],  PriceAction[candleCnt-1-6]['mid']['c'],
                      PriceAction[candleCnt-1-5]['mid']['c'], PriceAction[candleCnt-1-4]['mid']['c'], PriceAction[candleCnt-1-3]['mid']['c'],  PriceAction[candleCnt-1-2]['mid']['c'],  PriceAction[candleCnt-1-1]['mid']['c']])
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
#　過去の価格のAVG         ＃
#*************************＃
def AvgCal(statday,cntday):
  cnt = 0
  sum = 0
  while cnt < cntday:
    sum += round(float(PriceAction[statday - cnt]['mid']['c']),3)
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
    while cnt < candleCnt:
      np=float(PriceAction[candleCnt - 1 - cnt]['mid']['c'])
      if cnt < (9 - 1):
        avg9  = 0
        avg12 = 0
        avg26 = 0
      elif cnt == (9 - 1):
        avg9  = AvgCal(candleCnt - 1,9)
        avg12 = 0
        avg26 = 0      
      elif cnt < (12 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)#npの改良
        avg12 = 0
        avg26 = 0
      elif cnt == (12 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12  = AvgCal(candleCnt - 1,12)
        avg26 = 0
      elif cnt < (26 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12']  ) * 2 / (12 + 1),5)
        avg26 = 0
      elif cnt == (26 - 1):
        avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),5)
        avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12']  ) * 2 / (12 + 1),5)
        avg26  = AvgCal(candleCnt - 1,26)
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
    np = float(getNowPrice())#現在の価格
    macdtime=getNowTime()#現在の時間
    if macdtime != nowtime:
      avg9  = round(macd[0]['ema9']  + ( np - macd[0]['ema9'] ) * 2 / (9  + 1),)
      avg12 = round(macd[0]['ema12'] + ( np - macd[0]['ema12'] ) * 2 / (12 + 1),5)
      avg26 = round(macd[0]['ema26'] + ( np - macd[0]['ema26'] ) * 2 / (26 + 1),5)
      ma = round(avg12 - avg26,5)
      sig = round(macd[0]['sig'] + ( np - macd[0]['sig'] ) * 2 / (9 + 1),5) 
      macd.pop(candleCnt - 1)
      macd.insert(0,{"ema9":avg9,"ema12":avg12,"ema26":avg26,"macd":ma,"sig":sig})

      #else時間確定していない場合
      
    
  #return  macd


#*************************＃
#　　　　RSI          　　＃
#*************************＃
def RSI(day):
  cnt = 0

  psum = 0
  msum = 0
  while cnt < day:
    A=float(PriceAction[(candleCnt - 1) - cnt]['mid']['c'])*1000
    B=float(PriceAction[((candleCnt - 1) - cnt) - 1]['mid']['c'])*1000
    
    #データが大きいので現在の価格だけ再レスポンスし、最新のデータを取得する。
    #if (day - 1) - cnt == 0:
    #  A = float(getNowPrice())*1000
    
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
  #print(rsi)
  return rsi
#*************************＃
#　　 単純移動平均線       ＃
#*************************＃
def SimpleMovingAverage(day):
  avg = 0
  sum = 0
  cnt = 0
  while cnt < day:
    A = float(PriceAction[(candleCnt - 1) - cnt]['mid']['c'])*1000
    A = int(A)
    
    sum += A
    cnt += 1
    
  avg = float((sum / cnt) / 1000)
  avg = round(avg,3)
  
  return avg
  
#*************************＃
#　　トレード時間          ＃
#*************************＃
def NotTime():
  try:
    dt_now = datetime.datetime.now()

    if (21 <= dt_now.hour ) and (dt_now.hour <= 23):#21時から23時まで禁止
      bl = False
    elif (2 <= dt_now.hour) and (dt_now.hour <= 8):#2時から9時まで禁止
      bl = False
    elif (12 <= dt_now.hour) and (dt_now.hour <= 12):#12時から12時まで禁止
      bl = False
    else:
      bl = True
  except ZeroDivisionError:
    print("gettime error")

  bl = True#禁止時間でも強制的に許可する。（パフォーマンステスト用）
  return bl  

#*************************＃
#　   　  メイン          ＃
#*************************＃

#世界はアイと恐怖と欲望でできている

getOldCandlesClole(str(candleCnt),"M1")
timer = ""
posi_flag = 0
buyf = {"f1":0,"f2":0,"f3":0}
sellf = {"f1":0,"f2":0,"f3":0}
#MACD()

Debug_sell_cnt1 = 0
Debug_sell_cnt2 = 0
Debug_sell_cnt3 = 0
Debug_sell_cnt4 = 0

Debug_buy_cnt1 = 0
Debug_buy_cnt2 = 0
Debug_buy_cnt3 = 0
Debug_buy_cnt4 = 0

initsts = 0
while True:
  try:
    nowtime = getNowTime()#取引した時間
    getOldCandlesClole(str(candleCnt),"M1")
    NowPrice = float(getNowPrice()) #現在の価格情報を取得する
    bollinger=BollingerBands()
    rsi = RSI(14)
    SimpleAvg = SimpleMovingAverage(200)

    print("***************************************************")
    print()
    print("NowPrice(usd/jpy)  :",NowPrice)
    print()
    print("Upper Band2        : ",round(bollinger['Upper Band2'][19],3))
    print("Upper Band1        : ",round(bollinger['Upper Band1'][19],3))
    print("Lower Band1        : ",round(bollinger['Lower Band1'][19],3))
    print("Lower Band2        : ",round(bollinger['Lower Band2'][19],3))
    print("RSI                : ",rsi)
    print("SimpleMovingAverage: ",SimpleAvg)
    print("time               : ",NotTime())
    print("***************************************************")

    print("Debug_buy_cnt1",Debug_buy_cnt1)
    print("Debug_buy_cnt2",Debug_buy_cnt2)
    print("Debug_buy_cnt3",Debug_buy_cnt3)
    print("Debug_buy_cnt4",Debug_buy_cnt4)
    print("Debug_sell_cnt1",Debug_sell_cnt1)
    print("Debug_sell_cnt2",Debug_sell_cnt2)
    print("Debug_sell_cnt3",Debug_sell_cnt3)
    print("Debug_sell_cnt4",Debug_sell_cnt4)

    print("buyf[f1]",buyf["f1"])
    print("buyf[f2]",buyf["f2"])
    print("buyf[f3]",buyf["f3"])
    print("sellf[f1]",sellf["f1"])
    print("sellf[f2]",sellf["f2"])
    print("sellf[f3]",sellf["f3"])
    
    if (rsi <= 25) and (NowPrice >= SimpleAvg) and (True == NotTime()):
      buyf["f1"] = 1
    if (rsi >=32)and(buyf["f1"] == 1) :
      buyf["f2"] = 1
      buyf["f1"] = 0
      print("buy")
      OrderExchange("-10000","USD_JPY")
        
    if ((buyf["f2"] == 1)and
        ((NowPrice >= bollinger['Upper Band2'][19])or(rsi >= 65)or#利確
         (NowPrice <= bollinger['Lower Band2'][19])or((rsi <= 25)))) :#損切り
      
      if (NowPrice >= bollinger['Upper Band2'][19]):#利確
        Debug_buy_cnt1 += 1
      if (rsi >= 65):
        Debug_buy_cnt2 += 1
        
      if (NowPrice <= bollinger['Lower Band2'][19]):#損切り
        Debug_buy_cnt3 += 1
      if (rsi <= 25):
        Debug_buy_cnt4 += 1
        
        
      OrderExchange("10000","USD_JPY")
      buyf["f1"] = 0
      buyf["f2"] = 0
      buyf["f3"] = 0
      print("clear")


    if (rsi >= 75) and (NowPrice <= SimpleAvg)  and (True == NotTime()):
      sellf["f1"] = 1
    if (rsi <=68)and(sellf["f1"] == 1):
      sellf["f2"] = 1
      sellf["f1"] = 0
      print("sell")
      OrderExchange("10000","USD_JPY")
      
        
    if ((sellf["f2"] == 1)and
        ((NowPrice <= bollinger['Lower Band2'][19])or(rsi <= 35)or#利確
         (NowPrice >= bollinger['Upper Band2'][19])or((rsi >= 75)))) :#損切り
      
      if(NowPrice <= bollinger['Lower Band2'][19]):#利確
        Debug_sell_cnt1 += 1
      if(rsi <= 35):
        Debug_sell_cnt2 += 1
        
      if(NowPrice >= bollinger['Upper Band2'][19]):#損切り
        Debug_sell_cnt3 += 1
      if(rsi >= 75):
        Debug_sell_cnt4 += 1
        
      OrderExchange("-10000","USD_JPY")
      sellf["f1"] = 0
      sellf["f2"] = 0
      sellf["f3"] = 0
      print("clear")




    #MACD()
    #print(round(macd[0]['macd'],4))
  except :
    print("error!!!!!!!!!!!!!!")
    time.sleep(5)
    
  """
    if timer != nowtime:
      if True == NotTime():#取引する時間判定
        if NowPrice <= bollinger['Lower Band2'][19]:
          timer = getNowTime()#取引した時間
          OrderExchange("10000","USD_JPY")
          print("buy")
        elif NowPrice >= bollinger['Upper Band2'][19]:
          timer = getNowTime()#取引した時間
          OrderExchange("-10000","USD_JPY")
          print("sell")
        else:
          print("Non")
    time.sleep(1)
    print()
  """

    


#get['orderFillTransaction']['quotePL'] #損益を取得


#PositionTermination()

