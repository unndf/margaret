from keys.btcchina import Key
from urllib.parse import urlencode
from http.client import BadStatusLine
import http.client
import json

class Btcchina(object):
    def __init__(self,public_key,private_key):
        self.key = Key(public_key,private_key)

    def order_params(self,params):
        l = []
        order = ['tonce','accesskey','requestmethod','id','method','params']

        for field in order:
            l.append(field + '=' +str(params[field]))

        #join the list with '&' and replace '[', ']' and space
        return ('&'.join(l)).replace('[','').replace(']','').replace(' ','')

    def _public_request(self,method):
        status_code = 0
        while status_code != 200:
            conn = http.client.HTTPSConnection("data.btcchina.com")
            conn.request("GET", method)
            try:
                resp = conn.getresponse()
                status_code = resp.status
            except Exception:
                print("Error")

        st = str(resp.read().decode('utf-8'))
        return json.loads(st)

    def _private_request(self,method,params):
        status_code = 0
        while status_code != 200:
            conn = http.client.HTTPSConnection("api.btcchina.com")
            tonce = self.key.get_tonce()
            params = {"method":method,\
                      "tonce": tonce,\
                      "accesskey": self.key.BTCChina_api_key,\
                      "requestmethod":"post",\
                      "id":tonce,\
                      "params":params\
                      }

            pstring = self.order_params(params)
            header = self.key.gen_header(pstring)
            try:
                conn.request("POST", "/api_trade_v1.php" , json.dumps(params), header)
                resp = conn.getresponse()
                status_code = resp.status
            except Exception:
                print("Error occured")
        
        st = str(resp.read().decode('utf-8'))
        return(json.loads(st))

    def getinfo(self):
        method = "getAccountInfo"
        params = []
        return self._private_request(method,params)

    def buy(self,pair,amount=0.0,price=0.0):
        method = "buyOrder"
        params = [price,amount]
        self._private_request(method,params)

    def sell(self,pair,amount=0.0,price=0.0):
        method = "sellOrder"
        params = [price,amount]
        self._private_request(method,params)

    #parameter 'pair' is unused. It is to keep compatiblity with the the run method in the trade module
    def get_last(self,pair):
        method = "/data/ticker"
        return float(self._public_request(method)['ticker']['last'])

    def get_sell(self,pair):
        method = "/data/ticker"
        return float(self._public_request(method)['ticker']['sell'])

    def get_buy(self,pair):
        method = "/data/ticker"
        return float(self._public_request(method)['ticker']['buy'])
   
    def get_sales(self,pair):
        method = "/data/orderbook"
        sales = self._public_request(method)['asks']
        return [{'price':x[0],'amount':x[1]} for x in sales]

    def get_bids(self,pair):
        method = "/data/orderbook"
        bids = self._public_request(method)['bids']
        return [{'price':x[0],'amount':x[1]} for x in bids]
