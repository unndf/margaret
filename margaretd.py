import _thread
import configparser
from trader import Trader

#load_config() will attempt to read and parse the config file '.config' and create 'Trader' objects according to
#the parameters in the file. It will return a list of 'Trader' objects
def load_config():
    traders = []
    config = configparser.RawConfigParser()
    config.read('.config')
    sections = config.sections()
    for name in sections:

        indicator     =  config.get(name,'indicator')
        public_key    =  config.get(name,'public key')
        private_key   =  config.get(name,'private key')
        exchange      =  config.get(name,'exchange')
        pair          =  config.get(name,'pair')
        amount        =  config.get(name,'amount')
        charting      =  'candlestick'
        initial_wait  =  5
        period_length =  60

        #configure optional arguments in the config
        if config.has_option(name,'charting'):
            charting = config.get(name,'charting')
        if config.has_option(name,'initial_wait'):
            initial_wait = config.getint(name,'initial_wait')
        if config.has_option(name,'period_length'):
            period_length = getint(name,'period_length')

        trader = Trader(name,\
                        exchange,\
                        public_key,\
                        private_key,\
                        pair,\
                        amount,\
                        charting=charting,\
                        initial_wait=initial_wait,\
                        period_length=period_length)

        traders.append(trader)

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
            if config.has_option(name,'parameter'):
                para=config.getint(name,'parameter')
                trader.config_donchian_channels(para)
            else:
                trader.config_donchian_channels()

            trader.config_donchian_channels()
        
            trader.set_indicator('donchian_breakout')
        
        else:
            print("Error in Config file. The indicator is not valid. Exiting.")
            exit()

    return traders

if __name__ == '__main__':
    traders = load_config()
    for trader in traders:
        _thread.start_new_thread(trader.run,())

    while True:
            #run forever
            pass
