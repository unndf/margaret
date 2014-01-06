class Breakout(object):
    def __init__(self,trading_periods, parameter=10):
        self.upper = 0
        self.lower = 0
        self.parameter = parameter
        self.channels = []
        self.last = 0

        #calculate the channels for the trading periods already given
        i = 0
        while i < (len(trading_periods)) - parameter:
            highs = []
            lows  = []
            for price in trading_periods:
                highs.append(price['high'])
                lows.append(price['low'])

            highs = highs[i:i+parameter-1]
            lows  = lows[i:i+parameter-1]
            upper = self.calc_upper(highs)
            lower = self.calc_lower(lows)

            self.channels.append({'upper':upper,'lower':lower})
            i+=1

    def calc_upper(self,prices):
        return max(prices)

    def calc_lower(self,prices):
        return min(prices)

    #last periods must be the length of the longsma period
    def update(self,last_periods):
        last_periods = last_periods[:self.parameter-1]
        highs = []
        lows  = []
        for price in last_periods:
            highs.append(price['high'])
            lows.append(price['low'])

        upper = self.calc_upper(highs)
        lower = self.calc_lower(lows)

        self.channels.pop()
        self.channels.insert(0,{'upper':upper,'lower':lower})
        self.last = last_periods[0]['close']
    def get_signal(self):
        
        #Bullish, buy
        if self.last > self.channels[1]['upper']:
            return 'buy'
        #Bearish, sell
        elif self.last < self.channels[1]['lower']:
            return 'sell'
        else:
            return 'wait'
