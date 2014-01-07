from keys.btcekey import Key
from misc.backoff import Backoff
from urllib.parse import urlencode
from http.client import BadStatusLine

import json
import http.client
import json

class Btce(object):
    def __init__(self,public_key,private_key):
        self.conn = http.client.HTTPSConnection("btc-e.com")
        self.key = Key(public_key,private_key)

    def _private_request(self,params,header):
        status_code = 0
        conn = http.client.HTTPSConnection("btc-e.com")
        while status_code != 200:
            try:
                conn.request("POST","/tapi",params,header)
                response = conn.getresponse()
                status_code = response.status
            except Exception as e:
                #Do error handling
                print("Error occured during HTTP request. ", e.value)
        
        st = str(response.read().decode('utf-8'))
        return json.loads(st)

    def _public_request(self,method):
        status_code = 0
        conn = http.client.HTTPSConnection("btc-e.com")
        while status_code != 200:
            try:
                conn.request("GET","/api/2/"+method)
                response = conn.getresponse()
                status_code = response.status
            except Exception as e:
                #Do error handling
                print("Error occured during HTTP request. ", e.value)
        
        st = str(response.read().decode('utf-8'))
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
        method = pair+"/trades"
        trades = self._public_request(method)
        bids = []

        for trade in trades:
            if trade['trade_type'] == 'bid':
                bids.append(trade)
        
        return [ {'amount':x['amount'],'price':x['price']} for x in bids ]

    def get_sales(self,pair):
        method = pair+"/trades"
        trades = self._public_request(method)
        sales = []

        for trade in trades:
            if trade['trade_type'] == 'ask':
                sales.append(trade)
            
        return [ {'amount':x['amount'],'price':x['price']} for x in sales ]

    def get_last(self,pair):
        return self.get_ticker(pair)['last']

    def get_buy(self,pair):
        return self.get_ticker['buy']

    def get_sell(self,pair):
        return self.get_ticker(pair)['sell']

    def get_ticker(self,pair):
        method = pair+"/ticker"
        ticker = self._public_request(method)
        return ticker['ticker']
