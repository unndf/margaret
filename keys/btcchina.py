from urllib.parse import urlencode
from time import time
import hashlib
import hmac
import base64

class Key(object):
    def __init__(self,public,private):
        
        self.BTCChina_api_key = public
        self.BTCChina_api_secret_key = private

    def get_tonce(self):
        self.tonce = int(time()*1000000)
        return self.tonce

    def gen_header(self,params):
        H = hmac.new(self.BTCChina_api_secret_key.encode(),digestmod=hashlib.sha1)
        H.update(params.encode())
        sign = H.hexdigest()
        string = base64.b64encode((self.BTCChina_api_key + ':' + sign).encode() ).decode()
        auth_string = 'Basic ' + string
        return {"Content-type": "application/x-www-form-urlencoded",\
            "Authorization": auth_string,\
            "Json-Rpc-Tonce": self.tonce\
                }
