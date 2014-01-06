import sys
sys.path.append('..')
sys.path.append('../misc')

from keys.btcchina import Key
from misc.backoff import Backoff
from misc.backoff import Backoff
from urllib.parse import urlencode
from http.client import BadStatusLine

import json
import http.client
import json

class Btcchina(object):
    def __init__(self,public_key,private_key):
        self.conn = http.client.HTTPSConnection("api.btcchina.com",strict=False)
        self.dataconn = http.client.HTTPSConnection("data.btcchina.com",strict=False)
        self.key = Key(public_key,private_key)

    def order_params(self,params):
        l = []
        order = ['tonce','accesskey','requestmethod','id','method','params']

        for field in order:
            l.append(field + '=' +str(params[field]))

        #join the list with '&' and replace '[', ']' and space
        return ('&'.join(l)).replace('[','').replace(']','').replace(' ','')

    def getinfo(self):
        status_code = 0
        backoff = Backoff()
        while status_code != 200:
            tonce = self.key.get_tonce()
            params = {"method":"getAccountInfo",\
                      "tonce": tonce,\
                      "accesskey": self.key.BTCChina_api_key,\
                      "requestmethod":"post",\
                      "id":tonce,\
                      "params":[]\
                      }

            pstring = self.order_params(params)
            header = self.key.gen_header(pstring)
            self.conn.request("POST", "/api_trade_v1.php" , json.dumps(params), header)

            resp = self.conn.getresponse()
            status_code = resp.status
            backoff.sleep()
        
        st = str(resp.read().decode('utf-8'))
        return(json.loads(st))

    #parameter pair is unused. It is to keep compatiblity with the the run method in the trade module
    def get_last(self,pair):
        status_code = 0
        backoff = Backoff()
        self.dataconn.connect()
        while status_code != 200:
            
            self.dataconn.request("GET", "/data/ticker")
            
            try:
                resp = self.dataconn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return float((json.loads(st))['ticker']['last'])

    def get_sell(self,pair):
        status_code = 0
        backoff = Backoff()
        self.dataconn.connect()
        while status_code != 200:
            
            self.dataconn.request("GET", "/data/ticker")
            
            try:
                resp = self.dataconn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return float((json.loads(st))['ticker']['sell'])

    def get_buy(self,pair):
        status_code = 0
        backoff = Backoff()
        self.dataconn.connect()
        while status_code != 200:
            
            self.dataconn.request("GET", "/data/ticker")
            
            try:
                resp = self.dataconn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        return float((json.loads(st))['ticker']['buy'])
       
    def get_sales(self,pair):
        status_code = 0
        backoff = Backoff()
        self.dataconn.connect()
        while status_code != 200:
            
            self.dataconn.request("GET", "/data/orderbook")
            
            try:
                resp = self.dataconn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        sales = json.loads(st)['asks']
        
        return [{'price':x[0],'amount':x[1]} for x in sales]

    def get_bids(self,pair):
        status_code = 0
        backoff = Backoff()
        self.dataconn.connect()
        while status_code != 200:
            
            self.dataconn.request("GET", "/data/orderbook")
            
            try:
                resp = self.dataconn.getresponse()
                status_code = resp.status
            except BadStatusLine:
                status_code = 0

            backoff.sleep()

        st = str(resp.read().decode('utf-8'))
        bids = json.loads(st)['bids']
        return [{'price':x[0],'amount':x[1]} for x in bids]
