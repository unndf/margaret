from urllib.parse import urlencode
import hashlib
import hmac

class Key(object):
    def __init__(self,public,private):
        
        self.BTC_api_key = public
        self.BTC_api_secret_key = private
        self.name = public
        self._nonce = 0
        self.load_nonce()
    
    def get_nonce(self):
        temp = self.nonce
        self.nonce += 1
        self.save_nonce()
        return temp

    def load_nonce(self):
        try:
            save_file = open(self.name + '-nonce.txt','r')
            self.nonce = int(save_file.readline())
            save_file.close()
        except IOError:
            self.nonce = 0
            save_file = open(self.name + '-nonce.txt','w')
            save_file.write(str(self.nonce))
            save_file.close()
        except ValueError:
            self.nonce = 0

    def save_nonce(self):
        save_file = open(self.name +'-nonce.txt' ,'w')
        save_file.write(str(self.nonce))
        save_file.close()

    def gen_header(self,params):
        H = hmac.new(self.BTC_api_secret_key.encode(),digestmod=hashlib.sha512)
        H.update(params.encode())
        sign = H.hexdigest()

        return {"Content-type": "application/x-www-form-urlencoded",\
            "Key" : self.BTC_api_key ,\
            "Sign": sign\
                }
