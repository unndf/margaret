import _thread
import configparser
from trader import Trader

TRADERS = []

def load_config():
    
    config = configparser.RawConfigParser()
    config.read('.config')
    traders = config.sections()
    for name in traders:
        indicator = config.get(name,'indicator')
        public_key  =  config.get(name,'public key')
        private_key =  config.get(name,'private key')
        exchange    =  config.get(name,'exchange')
        pair        =  config.get(name,'pair')
        amount      =  config.get(name,'amount')

        trader = Trader(name,exchange,public_key,private_key,pair,amount)
        TRADERS.append(trader)
        
        if indicator == 'smacrossover':
            if config.has_option(name,'short') and config.has_option(name,'long'):
                ssma=config.getint(name,'short')
                lsma=config.getint(name,'long')
                trader.config_sma(ssma,lsam)
            else:
                trader.config_sma()
            
            trader.set_indicator('sma_crossover')

        elif indicator == 'emacrossover':
            if config.has_option(name,'short') and config.has_option(name,'long'):
                sema=config.getint(name,'short')
                lema=config.getint(name,'long')
                trader.config_ema(sema,lema)
            else:
                trader.config_ema()
    
            trader.set_indicator('ema_crossover')

        elif indicator == 'donchianbreakout':
            trader.config_donchian_channels()
        
            trader.set_indicator('donchian_breakout')

def start_traders():
    for trader in TRADERS:
        _thread.start_new_thread(trader.run,())

if __name__ == '__main__':
    load_config()
    start_traders()
    while True:
            pass
