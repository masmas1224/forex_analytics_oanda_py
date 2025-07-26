class STRUCT: #クラス作成
    timer = ""
    posi_flag = 0
    buyf = {"f1":0,"f2":0,"f3":0}
    sellf = {"f1":0,"f2":0,"f3":0}
    Debug_sell_cnt1 = 0
    Debug_sell_cnt2 = 0
    Debug_sell_cnt3 = 0
    Debug_sell_cnt4 = 0
    Debug_buy_cnt1 = 0
    Debug_buy_cnt2 = 0
    Debug_buy_cnt3 = 0
    Debug_buy_cnt4 = 0
    vix_f1 = 0
    vix_f2 = 0
    vix_f3 = 0
    vix_f4 = 0
    vix_f5 = 0
    vix_time = ""
    initsts = 1
    
    vixmin = 255
    
    global PriceAction
    nowtime = ""
    macdtime = ""
    accountID = ""
    access_token = ''
    
    candleCnt = 400
    #def __init__(self): #コンストラクタ
