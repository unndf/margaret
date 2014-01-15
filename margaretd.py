#!/usr/bin/env python3
import json
from trader import Trader

def indicator_config(trader,indicator):
    if "smacrossover" in indicator:
        p = indicator['smacrossover']
        trader.config_sma(shortsma=p['short'], longsma=p['long'])
    if "emacrossover" in indicator:
        p = indicator['emacrossover']
        trader.config_ema(shortema=p['short'], longema=p['long'])
    if "donchianchannels" in indicator:
        p = indicator['donchianchannels']
        trader.config_donchian_channels(parameter=p['parameter'])


def load_config():
    required_params = {"exchange":None,"public_key":None,"private_key":None,"pair":None,"amount":None}
    optional_params = {"stoploss":7,"charting":"candlestick","period_length":60}
    traders = []
    
    config_file = open('margaret_config.json','r')
    config = json.loads(config_file.read())
    config_file.close()

    for name,params in config.items():
        for key in required_params:
            required_params[key] = params[key]
        
        for key in optional_params:
            if key in params:
                optional_params[key] = params[key]
        
        r = required_params
        o = optional_params
        trader = Trader(name,r['exchange'],r['public_key'],r['private_key'],r['pair'],r['amount'],
                        period_length=o['period_length'],\
                        charting=o['charting'],\
                        stoploss=o['stoploss'])
        
        try:
            trader.restore(trader.get_historical())
        except:
            pass

        indicator_config(trader,params['indicator_config'])
        
        
        i = params['indicator']
        if len(i) == 2:
            indicators = {"emacrossover":trader.ema,"smacrossover":trader.sma,"donchianchannels":trader.donchian_breakout}
            trader.config_dual_indicator(indicators[i[0]],indicators[i[1]])
            trader.set_indicator("dual_indicator")
        else:
            trader.set_indicator(i[0])
        
        traders.append(trader)

    return traders

if __name__ == "__main__":
    traders = load_config()
    for trader in traders:
        trader.start()
