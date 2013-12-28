from time import time
from time import strftime
from time import sleep
from key import Key
from urllib.parse import urlencode
import json
import hashlib
import hmac

import http.client
import json

VALID_PAIRS= \
    [   "btc_usd",\
        "btc_rur",\
        "btc_eur",\
        "ltc_btc",\
        "ltc_rur",\
        "ltc_eur",\
        "nmc_btc",\
        "nmc_usd",\
        "nvc_btc",\
        "nvc_usd",\
        "usd_rur",\
        "usd_rur",\
        "eur_usd",\
        "trc_btc",\
        "ppc_btc",\
        "ppc_usd",\
        "ftc_btc",\
        "xpm_btc"]

#This is the base trade class. It contains the basic methods for accessing the bte-e public and private api
#It will not perform trades by itself, and doesn't have a 'run' method for trading.

#__init__() parameters:
#   pair:
#       type: String
#       The currency pair to be traded
#   log:
#       type: String
#       This is the log file that the trade object will write to
#   public_key:
#       type: String
#       btc-e public key
#   private_key: 
#       type: String
#       btc-e private key
#   update_interval:
#       type: Float
#       The amount of time in seconds to wait before getting new ticker information from the btc-e ticker
#   trade_period:
#       type: Float
#       This is the amount of time in seconds in a trading period. For example, the default 60 would mean every 
#       entry in the self.history list is a minute apart
#   amount:
#       type: Float
#       The amount of money that will be traded. defaulted 0

class Trade(object):
    def __init__(self,\
                 pair,\
                 log,\
                 public_key,\
                 private_key,\
                 update_interval=2,\
                 trade_period=60,\
                 amount = 0.0):

        self.key = Key(public=public_key,private=private_key,name=log)
        self.pair = pair
        self.update_interval = update_interval
        self.trade_period = trade_period/2
        self.trade_amount = amount
        self.log = log+".log"
        self.bid_orders   = []
        self.sell_orders  = []
        self.history = [ {'high':0,'low':0,'avg':0,'open':0,'close':0}] * 1000

    def get_last(self):
        status_code = 0 
        while status_code != 200:
            conn = http.client.HTTPSConnection("btc-e.com")
            conn.request("GET", "/api/2/" + self.pair + "/ticker")
            
            resp = conn.getresponse()
            status_code = resp.status
            resp = resp.read().decode("utf-8")
            conn.close()

            if status_code != 200:
                self.append_log(str(resp.status) + ' ' + str(resp.reason))
                backoff_time *= 2
                sleep(backoff_time)
 
        return (json.loads(resp))['ticker']['last']

    def get_trades(self):
        status_code = 0
        backoff_time = 1
        while status_code != 200:
            conn = http.client.HTTPSConnection("btc-e.com")
            conn.request("GET", "/api/2/" + self.pair + "/trades")

            resp = conn.getresponse()
            status_code = resp.status
            resp = resp.read().decode("utf-8")
            conn.close()

            if status_code != 200:
                self.append_log(str(resp.status) + ' ' + str(resp.reason))
                backoff_time *= 2
                sleep(backoff_time)
  
        trades = json.loads(resp)
        
        sell_orders = []
        bid_orders  = []

        for trade in trades:
            if trade['trade_type'] == 'ask':
                sell_orders.append(trade)
            elif trade['trade_type'] == 'bid':
                bid_orders.append(trade)


        self.sell_orders = sell_orders
        self.bid_orders  = bid_orders
    
    def optimal_sell(self):
        self.get_trades()
        sales = []
        for sale in self.sell_orders:
            if sale['amount'] >= self.trade_amount:
                sales.append(sale)
        
        bid = 0 
        for sale in sales:
            if sale['price'] < bid or bid == 0:
                bid  = sale['price']

        return bid

    def optimal_bid(self):
        self.get_trades()
        bids = []
        for bid in self.bid_orders:
            if bid['amount'] >= self.trade_amount:
                bids.append(bid)
        
        sell = 0 
        for bid in bids:
            if bid['price'] > sell or sell == 0:
                sell = bid['price']


        return sell

    def getInfo(self):
        params = {"method":"getInfo",\
              "nonce": self.key.nonce}
       
        params = urlencode(params)
        
        header = self.key.gen_header(params)
        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi" , params, header)

        response = conn.getresponse()

        print(response.status,response.reason)
        st = str(response.read().decode('utf-8'))
        print(json.loads(st))

        response.close()

        self.key.inc_nonce()

    def tradeHistory(self):
        params = {"method":"TradeHistory",\
              "nonce": self.key.nonce}

        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi" , params, self.key.header)

        self.key.inc_nonce()

    def transHistory(self):
        params = {"method":"TradeHistory",\
              "nonce": key.nonce}

        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi" , params, header)

        self.key.inc_nonce()

    def activeOrders(self):
        params = {"method":"TradeHistory",\
              "nonce": key.nonce}

        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi" , params, self.key.header)

        self.key.inc_nonce()

    def trade(self,rate=0.0,transaction='buy'):
        status_code = 0
        backoff_time = 1
        while status_code != 200:
            params = {"method":"Trade",\
                  "nonce":self.key.nonce,\
                  "pair":self.pair,\
                  "amount":self.trade_amount,\
                  "rate":rate,\
                  "type":transaction\
                  }
            
            params = urlencode(params)
            
            header = self.key.gen_header(params)
            conn = http.client.HTTPSConnection("btc-e.com")
            conn.request("POST", "/tapi" , params, header)

            resp = conn.getresponse()
            status_code = resp.status

            if status_code != 200:
                self.append_log(str(resp.status) + ' ' + str(resp.reason))
                sleep(backoff_time)
                backoff_time *= 2

            resp.close()
            self.key.inc_nonce()

    def cancelOrder(self,order_id):
        params = {"method":"TradeHistory",\
            "nonce": key.nonce}

        conn = http.client.HTTPSConnection("btc-e.com")
        conn.request("POST", "/tapi" , params, self.key.header)

        self.key.inc_nonce()

    def append_log(self,text):
        log = open(self.log,'a+')
        log.write(strftime('%I:%M:%S') + ' : ' + text + '\n')
        log.close()
