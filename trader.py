from threading import Thread
from time import time
from time import sleep
from time import strftime
from exchanges.btce import Btce
from methods.donchianchannels import Breakout
from methods.smacrossover import SMAcrossover
from methods.emacrossover import EMAcrossover
from methods.trailingstop import Trailingstop
from exchanges.btcchina import Btcchina

#from exchanges.cryptsy import Cryptsy
#SOON......


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
'btce':Btce,\
'btcchina':Btcchina\
}
INDICATORS = {\
'sma_crossover': SMAcrossover,\
'ema_crossover': EMAcrossover,\
'donchain_breakout': Breakout,\
}

class Trader(Thread):
    def __init__(self,name,exchange,public_key,private_key,pair,amount,\
                 datumsize=1000,\
                 period_length=60,\
                 charting='candlestick',\
                 initial_wait=5,\
                 update_interval=5,\
                 stoploss=7):
        
        Thread.__init__(self)
        self.name = name
        self.exchange = EXCHANGES[exchange](public_key,private_key)
        self.amount = amount
        self.pair = pair
        self.period_length = period_length
        self.charting = charting
        self.initial_wait = initial_wait
        self.update_interval = update_interval
        self.indicators = {}
        self.datum = [{'open':0,'close':0,'high':0,'low':0}] * datumsize
        self.trade_history = [{'buy':0,'sell':0,'profit':0}] * datumsize
        self.stop = True
        self.stoploss_percentage = stoploss

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
        active_trade = False
        profits = 0
        stoploss = Trailingstop(self.datum[0]['close'],self.stoploss_percentage)

        while not self.stop:
            signal = self.indicator.get_signal()
            if signal == 'buy' and not active_trade:
                #buy
                self.buy()
                stoploss = Trailingstop(self.datum[0]['close'],self.stoploss_percentage)
                active_trade = True

            elif signal == 'sell' and active_trade:
                #sell
                self.sell()
                active_trade = False

            elif signal == 'wait' and active_trade:
                if self.datum[0]['close'] <= stoploss.stop:
                    self.sell()
                    active_trade = False
                else:
                    print('[' + self.name + ']: is waiting. Last:'+str(self.datum[0]))
            elif signal =='wait':
                print('[' + self.name + ']: is waiting. Last:'+str(self.datum[0]))
            
            start = time()
            prices = []
            while(time() < (start + self.period_length)):
                last = self.exchange.get_last(self.pair)
                prices.append(last)
                sleep(self.update_interval)
            
            self.chart(prices)
            self.indicator.update(self.datum)
            stoploss.update(self.datum[0]['close'])
    
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

    def append_log(self,message):
        cwd = os.path.dirname(__file__)
        log = open(cwd+ "/logs/" + self.name+'.log', 'a')
        log.write(strftime("%B %d @ %H:%M > ")+ message +'\n')

    def sell(self):
        price = self.exchange.get_sell(self.pair)
        self.exchange.sell(self.pair,self.amount,price)

        self.trade_history[0]['sell'] = price
        self.trade_history[0]['profit'] = (price - self.trade_history[0]['buy']) * self.amount
        
        print('[' + self.name + ']: recieved signal to sell')
        print("profits: ", self.trade_history[0]['profit'])
        
        self.append_log("Sell signal recieved\n" +\
                        "Selling :"+str(self.amount) + str(self.pair[:3]) +\
                        ' @ ' + str(price) + str(self.pair[4:]) + '\n' +\
                        "Profit :" + str(self.trade_history[0]['profit']) + '\n' +\
                        "Cumulative Profit: " + str(sum([x['profit'] for x in self.trade_history])) + str(self.pair[4:]) ) 

    
    def buy(self): 
        price = self.exchange.get_buy(self.pair)
        self.exchange.buy(self.pair,self.amount,price)

        print('[' + self.name + ']: recieved signal to buy')
        self.append_log("Buy signal recieved\n"+"Buying :"+str(self.amount) + str(self.pair[:3]) +\
                        ' @ ' + str(price) + str(self.pair[4:]) )
        
        self.trade_history.pop()
        self.trade_history.insert(0,{'buy':0.0,'sell':0.0,'profit':0.0})
        self.trade_history[0]['buy'] = price 
