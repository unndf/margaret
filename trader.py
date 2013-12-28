import sys
sys.path.append('./misc')

from time import time
from time import sleep
from exchanges.btce import Btce
from methods.donchianchannels import Breakout
from methods.smacrossover import SMAcrossover
from methods.emacrossover import EMAcrossover

#SOON......
#from exchanges.btcchina import Btcchina
#from exchanges.cryptsy import Cryptsy


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

EXCHANGES = {\
'btce':Btce\
}
INDICATORS = {\
'sma_crossover': SMAcrossover,\
'ema_crossover': EMAcrossover,\
'donchain_breakout': Breakout,\
}

class Trader(object):
    def __init__(self,exchange,public_key,private_key,pair,amount,\
                 datumsize=1000,\
                 period_length=60,\
                 charting='candlestick',\
                 inital_wait=5,\
                 update_interval=5):

        self.exchange = EXCHANGES[exchange](public_key,private_key)
        self.amount = amount
        self.pair = pair
        self.period_length = period_length
        self.charting = charting
        self.inital_wait = inital_wait
        self.update_interval = update_interval
        self.indicators = {}
        self.datum = [{'open':0,'close':0,'high':0,'low':0}] * datumsize
        self.stop = True
    
    def config_sma(self,shortsma=7,longsma=30):
        self.sma = SMAcrossover(self.datum,shortsma=shortsma,longsma=longsma)
        self.indicators['sma_crossover'] = self.sma

    def config_ema(self,shortema=7,longema=30,coefficient=0.2):
        self.ema = EMAcrossover(self.datum,shortema=shortema,longema=longema,coefficient=coefficient)
        self.indicators['ema_crossover'] = self.ema

    def config_donchian_channels(self,parameter=10):
        self.donchian_breakout = Breakout(self.datum,parameter=parameter)
        self.indicators['donchian_breakout'] = self.donchian_breakout

    def set_indicator(self,indicator):
        self.indicator = self.indicators[indicator]

    def run(self):
        self.stop = False
        while not self.stop:
            signal = self.indicator.get_signal()
            if signal == 'buy':
                #buy
                #self.exchange.buy()
                print('BUY')
            elif signal == 'sell':
                #sell
                #self.exchange.sell()
                print('SELL')
            elif signal == 'wait':
                #wait
                print('WAIT')
                
            start = time()
            prices = []
            while(time() < (start + self.period_length)):
                last = self.exchange.get_last(self.pair)
                prices.append(last)
                sleep(self.update_interval)
            
            self.chart(prices)
            self.indicator.update(self.datum)
            
    def prep_period(self):
        for i in range(self.initial_wait):
            start = time()
            prices = []
            while (time() < start + self.period_length):
                last = self.exchange.get_last(self.pair)
                prices.append(last)
                sleep(self.update_interval)
            self.chart(prices)

    def chart(self,datum):
        if self.charting == 'candlestick':
            mopen  = datum[0]
            mclose = datum[len(datum)-1]
            mhigh  = max(datum)
            mlow   = min(datum)
        elif self.charting == 'heikin-ashi':
            mclose = (datum[0] + datum[len(datum)-1] + max(datum) + min(datum)) / 4
            mopen  = (self.datum[0]['open'] + self.datum[0]['close']) / 2
            mhigh  = max(max(datum),mopen,mclose)
            mlow   = min(min(datum),mopen,mclose)

        self.datum.pop()
        self.datum.insert(0,{'high':mhigh,'low':mlow,'open':mopen,'close':mclose})
#        bid = 0 
#        for sale in sales:
#            if sale['price'] < bid or bid == 0:
#                bid  = sale['price']

#        return bid

#    def optimal_bid(self):
#        sell = 0 
#        for bid in bids:
#            if bid['price'] > sell or sell == 0:
#                sell = bid['price']

#        return sell
