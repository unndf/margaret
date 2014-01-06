import sys
sys.path.append('..')
sys.path.append('../misc')

from keys.btcekey import Key
from misc.backoff import Backoff
from urllib.parse import urlencode
from http.client import BadStatusLine

import json
import http.client
import json

class Btce(object):
    def __init__(self,public_key,private_key):
        self.conn = http.client.HTTPSConnection("btc-e.com",strict=False)
        self.key = Key(public_key,private_key)

    def _private_request(self,params,header):
        status_code = 0
        conn = http.client.HTTPSConnection("btc-e.com")
        while status_code != 200:
            try:
                conn.request("POST","/tapi",params,header)
                response = conn.getresponse()
                self.status = response.status
            except Exception as e:
                #Do error handling
                print("Error occured during HTTP request. ", e.value)
        
        st = str(resp.read().decode('utf-8'))
        return json.loads(st)

    def getinfo(self):
        params = {"method":"getInfo",\
                  "nonce": self.key.get_nonce()}
        params = urlencode(params)
        header = self.key.gen_header(params)
        return self._private_request(params,header)

    def activeorders(self,pair):
        params = {"method":"ActiveOrders",\
                  "pair":pair,\
                  "nonce": self.key.get_nonce()}
        params = urlencode(params)
        header = self.key.gen_header(params)
        return self._private_request(params,header)

    def buy(self,pair,amount=0.0,price=0.0):
        params = {"method":"Trade",\
              "nonce":self.key.get_nonce(),\
              "pair":pair,\
              "amount":amount,\
              "rate":price,\
              "type":'buy'\
              }
        params = urlencode(params)
        header = self.key.gen_header(params)
        return self._private_request(params,header)

    def sell(self,pair,amount=0.0,price=0.0):
        params = {"method":"Trade",\
              "nonce":self.key.get_nonce(),\
              "pair":pair,\
              "amount":amount,\
              "rate":price,\
              "type":'sell'\
              }
        params = urlencode(params)
        header = self.key.gen_header(params)
        return self._private_request(params,header)
    
    def get_bids(self,pair):
        status_code = 0
        backoff = Backoff()
        self.conn.connect()
        while status_code != 200:

            self.conn.request("GET", "/api/2/"+ pair + "/trades")
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        raw = json.loads(st)
        bids = []

        for trade in raw:
            if trade['trade_type'] == 'bid':
                bids.append(trade)
        
        return [ {'amount':x['amount'],'price':x['price']} for x in bids ]

    def get_sales(self,pair):
        status_code = 0
        backoff = Backoff()
        self.conn.connect()
        while status_code != 200:

            self.conn.request("GET", "/api/2/"+ pair + "/trades")
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        raw = json.loads(st)
        sales = []

        for trade in raw:
            if trade['trade_type'] == 'ask':
                sales.append(trade)
            
        return [ {'amount':x['amount'],'price':x['price']} for x in sales ]

    def get_last(self,pair):
        status_code = 0
        backoff = Backoff()
        self.conn.connect()
        while status_code != 200:
            
            self.conn.request("GET", "/api/2/" + pair + "/ticker")
            
            try:
                resp = self.conn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return (json.loads(st))['ticker']['last']

    def get_buy(self,pair):
        return self.get_ticker['buy']

    def get_sell(self,pair):
        return self.get_ticker(pair)['sell']

    def get_ticker(self,pair):
        status_code = 0
        backoff = Backoff()
        #self.conn.connect()
        self.conn = http.client.HTTPSConnection("btc-e.com",strict=False)
        while status_code != 200:
            
            self.conn.request("GET", "/api/2/" + pair + "/ticker")
            
            try:
                resp = self.conn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return (json.loads(st))['ticker']
