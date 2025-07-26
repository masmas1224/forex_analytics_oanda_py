
import datetime
import time

import macd
import price
import bollingerbands
import SimpleMovingAverage
import rsi

import STRUCT as St

st=St.STRUCT()

global PriceAction
nowtime = ""
macdtime = ""
accountID = ""
access_token = ''
  
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

  #bl = True#禁止時間でも強制的に許可する。（パフォーマンステスト用）
  return bl  

#*************************＃
#　   　  メイン          ＃
#*************************＃

#price.getOldCandlesClole(str(price.candleCnt),"M1")
price.getOldCandlesClole(str(price.candleCnt),"M1")

st.initsts = 1
while True:
  try:

    price.getOldCandlesClole(str(price.candleCnt),"M1")
    nowtime = price.getNowTime()#取引した時間
    NowPrice = float(price.getNowPrice()) #現在の価格情報を取得する
    NowRsi = rsi.RSI(14)
    SimpleAvg = SimpleMovingAverage.AvgPrice(75)

    if nowtime != st.timer:
      print("Before round time >> After round time time")
      st.timer=nowtime
      price.getOldCandlesClole_("2030","M1")
      vixAvg = bollingerbands.BBAverageVolatility()
    bollinger=bollingerbands.BBprice()
    vix = bollingerbands.BBVolatility()
    
    
    print("***************************************************")
    print()
    print("NowPrice(usd/jpy)  :",NowPrice)
    print()
    print("Upper Band2        : ",round(bollinger['Upper Band2'][19],3))
    print("Upper Band1        : ",round(bollinger['Upper Band1'][19],3))
    print("Lower Band1        : ",round(bollinger['Lower Band1'][19],3))
    print("Lower Band2        : ",round(bollinger['Lower Band2'][19],3))

    print("vix                : ",vix)
    print("vixAvg             : ",vixAvg)
    print("vixAvg*0.4        : ",round(vixAvg*0.4,3))
    print()
    print("RSI                : ",NowRsi)
    print("SimpleMovingAverage: ",SimpleAvg)
    print("time               : ",NotTime())
    print()
    print("***************************************************")
    
    vixavg_hosu=round(vixAvg*0.4,3)

    if((vix <= vixavg_hosu)and
       (st.vix_f2 == 0)and(st.vix_f3 == 0)and(st.vix_f4 == 0)and(st.vix_f5 == 0)):
      st.vix_f1 = 1
      st.vix_f2 = 0
      st.vix_f3 = 0
      st.vix_f4 = 0
      st.vix_f5 = 0
      if st.vixmin >= vix:
        st.vixmin = vix

    if(vix >= st.vixmin*1.2) and (st.vix_f1 == 1):
      st.vix_f1 = 0
      st.vix_f2 = 1
      st.vix_f3 = 0
      st.vix_f4 = 0
      st.vix_f5 = 0

    if(st.vix_f2 == 1):
      if(NowPrice > bollinger['Upper Band1'][19]):
        price.OrderExchange("100000","USD_JPY")
        st.vix_time = nowtime
        st.vix_f1 = 0
        st.vix_f2 = 0
        st.vix_f3 = 1
        st.vix_f4 = 0
        st.vix_f5 = 0
      if(NowPrice < bollinger['Lower Band1'][19]):
        price.OrderExchange("-100000","USD_JPY")
        st.vix_time = nowtime
        st.vix_f1 = 0
        st.vix_f2 = 0
        st.vix_f3 = 0
        st.vix_f4 = 1
        st.vix_f5 = 0

    if(NowPrice >= bollinger['Upper Band2'][19])and(st.vix_f3 ==1):
      st.vix_f5 = 1

    if(NowPrice<=bollinger['Lower Band2'][19])and(st.vix_f4 == 1):
      st.vix_f5 = 1

    print(st.vix_f1,st.vix_f2,st.vix_f3,st.vix_f4,st.vix_f5)
    if(st.vix_f3 == 1)or(st.vix_f4 == 1):
      
      Oldbollinger=bollingerbands.BBOldprice_(0)
    
      oldBBup=round(float(Oldbollinger['Upper Band1'][19]),3)
      oldBBlow=round(float(Oldbollinger['Lower Band1'][19]),3)
      oldprice=round(float(price.PriceAction[price.candleCnt - 2]['mid']['c']),3)
      
      if(st.vix_f5 == 1):
        if(st.vix_f3 == 1) and ((oldprice >= oldBBup) or (NowPrice < bollinger['Rolling Mean'][19]) ):
          price.OrderExchange("-100000","USD_JPY")
          st.vix_f1 = 0
          st.vix_f2 = 0
          st.vix_f3 = 0
          st.vix_f4 = 0
          st.vix_f5 = 0
          st.vixmin = 255
        elif(st.vix_f4 == 1) and ((oldprice <= oldBBlow) or (NowPrice > bollinger['Rolling Mean'][19])):
          price.OrderExchange("100000","USD_JPY")
          st.vix_f1 = 0
          st.vix_f2 = 0
          st.vix_f3 = 0
          st.vix_f4 = 0
          st.vix_f5 = 0
          st.vixmin = 255
      else:
        if(st.vix_f3 == 1) and (NowPrice <= bollinger['Lower Band2'][19]):
          price.OrderExchange("-100000","USD_JPY")
          st.vix_f1 = 0
          st.vix_f2 = 0
          st.vix_f3 = 0
          st.vix_f4 = 0
          st.vix_f5 = 0
          st.vixmin = 255
        elif(st.vix_f4 == 1) and (NowPrice >= bollinger['Upper Band2'][19]):
          price.OrderExchange("100000","USD_JPY")
          st.vix_f1 = 0
          st.vix_f2 = 0
          st.vix_f3 = 0
          st.vix_f4 = 0
          st.vix_f5 = 0
          st.vixmin = 255


    #"""
    #---------------------------------------------------------------------------
    #---------------------------------------------------------------------------
    """
    if (NowRsi <= 25) and (NowPrice >= SimpleAvg):
      st.buyf["f1"] = 1
    if (NowRsi >=32)and(st.buyf["f1"] == 1) :
      st.buyf["f2"] = 1
      st.buyf["f1"] = 0
      print("buy")
      price.OrderExchange("-100000","USD_JPY")
        
    if ((st.buyf["f2"] == 1)and
        ((NowPrice >= bollinger['Upper Band2'][19])or(NowRsi >= 65)or#損切り
         (NowPrice <= bollinger['Lower Band2'][19])or((NowRsi <= 25)))): #利確
      
      if (NowPrice >= bollinger['Upper Band2'][19]):#利確
        st.Debug_buy_cnt1 += 1
      if (NowRsi >= 65):
        st.Debug_buy_cnt2 += 1
        
      if (NowPrice <= bollinger['Lower Band2'][19]):#損切り
        st.Debug_buy_cnt3 += 1
      if (NowRsi <= 25):
        st.Debug_buy_cnt4 += 1
        
        
      price.OrderExchange("100000","USD_JPY")
      st.buyf["f1"] = 0
      st.buyf["f2"] = 0
      st.buyf["f3"] = 0
      print("clear")


    if (NowRsi >= 75) and (NowPrice <= SimpleAvg):
      st.sellf["f1"] = 1
    if (NowRsi <=68)and(st.sellf["f1"] == 1):
      st.sellf["f2"] = 1
      st.sellf["f1"] = 0
      print("sell")
      price.OrderExchange("100000","USD_JPY")
      
        
    if ((st.sellf["f2"] == 1)and
        ((NowPrice <= bollinger['Lower Band2'][19])or(NowRsi <= 35)or#損切り
         (NowPrice >= bollinger['Upper Band2'][19])or((NowRsi >= 75)))) :#利確
      
      if(NowPrice <= bollinger['Lower Band2'][19]):#利確
        st.Debug_sell_cnt1 += 1
      if(NowRsi <= 35):
        st.Debug_sell_cnt2 += 1
        
      if(NowPrice >= bollinger['Upper Band2'][19]):#損切り
        st.Debug_sell_cnt3 += 1
      if(NowRsi >= 75):
        st.Debug_sell_cnt4 += 1
        
      price.OrderExchange("-100000","USD_JPY")
      st.sellf["f1"] = 0
      st.sellf["f2"] = 0
      st.sellf["f3"] = 0
      print("clear")
    """
    #---------------------------------------------------------------------------
    
    #MACD()
    #print(round(macd[0]['macd'],4))
    print()
    print()
    print()
    print()
  except :
    print("error!!!!!!!!!!!!!!")
    time.sleep(1)

#get['orderFillTransaction']['quotePL'] #損益を取得


#PositionTermination()

