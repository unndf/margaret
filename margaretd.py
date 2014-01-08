#!/usr/bin/env python3
import _thread
from misc.config import load_config

def start(trader):
    trader.prep_period()
    trader.run()

if __name__ == '__main__':
    traders = load_config()
    for trader in traders:
        trader.start()

    while True:
            #run forever
            pass
