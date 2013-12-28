import sys
sys.path.append('..')
sys.path.append('../misc')

from keys.btcekey import Key
from backoff import Backoff
from urllib.parse import urlencode

import json
import http.client
import json

class Btce(object):
    def __init__(self,public_key,private_key):
        self.conn = http.client.HTTPSConnection("btc-e.com")
        self.key = Key(public_key,private_key)

    def getinfo(self):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            params = {"method":"getInfo",\
                      "nonce": self.key.get_nonce()}
           
            params = urlencode(params)
            
            header = self.key.gen_header(params)
            self.conn.request("POST", "/tapi" , params, header)

            resp = self.conn.getresponse()
            status_code = resp.status

            backoff.sleep()
        
        st = str(resp.read().decode('utf-8'))
        return(json.loads(st))


    def activeorders(self,pair):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            params = {"method":"ActiveOrders",\
                      "pair":pair,\
                      "nonce": self.key.get_nonce()}
            params = urlencode(params)

            header = self.key.gen_header(params)
            self.conn.request("POST", "/tapi" , params, header)
            
            resp = self.conn.getresponse()
            status_code = resp.status

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return(json.loads(st))

    def trade(self,pair,rate=0.0,transaction='buy',amount=0.0):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            params = {"method":"Trade",\
                  "nonce":self.key.get_nonce(),\
                  "pair":pair,\
                  "amount":amount,\
                  "rate":rate,\
                  "type":transaction\
                  }
            
            params = urlencode(params)
            
            header = self.key.gen_header(params)
            self.conn = http.client.HTTPSConnection("btc-e.com")
            self.conn.request("POST", "/tapi" , params, header)

            resp = self.conn.getresponse()
            status_code = resp.status

            if status_code != 200:
                self.append_log(str(resp.status) + ' ' + str(resp.reason))
                backoff.sleep()

    def cancelorder(self,order_id):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            params = {"method":"CancelOrder",\
                      "nonce": self.key.get_nonce()}
            params = urlencode(params)

            header = self.key.gen_header(params)
            self.conn.request("POST", "/tapi" , params, header)
            
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return json.loads(st)

    def getbids(self,pair):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:

            self.conn.request("GET", "/api/2/"+ pair + "/trades")
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        raw_trades = json.loads(st)
        bids = []

        for trade in raw_trades:
            if trade['trade_type'] == 'bid':
                bids.append(trade)

        return bids

    def getsales(self,pair):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:

            self.conn.request("GET", "/api/2/"+ pair + "/trades")
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        raw_trades = json.loads(st)
        sales = []

        for trade in raw:
            if trade['trade_type'] == 'ask':
                sales.append(trade)

        return sales

    def get_last(self,pair):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            
            self.conn.request("GET", "/api/2/" + pair + "/ticker")
            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return (json.loads(st))['ticker']['last']
