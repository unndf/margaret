class SMAcrossover(object):
    def __init__(self,trading_periods,shortsma=7,longsma=30):
        self.shortsma = shortsma
        self.longsma  = longsma
        self.sma = []

        #calculate the sma for the trading periods already given
        i = 0
        while i < ((len(trading_periods)) - longsma):
            raw = trading_periods[i:i+longsma-1]
            prices = []
            for price in raw:
                prices.append(price['close'])

            lsma = self.calc_sma(prices)
            ssma = self.calc_sma(prices[:shortsma-1])

            self.sma.append({'shortsma':ssma,'longsma':lsma})
            i+=1

    def calc_sma(self,prices):
        total = 0
        for price in prices:
            total += price

        return total/(len(prices))
    
    #last periods must be the length of the longsma period
    def update(self,last_periods):
        prices = []
        for price in last_periods:
            prices.append(price['close'])

        prices = prices[:self.longsma-1]
        ssma = self.calc_sma(prices)
        lsma = self.calc_sma(prices[:self.shortsma-1])
        
        self.sma.pop()
        self.sma.insert(0,{'shortsma':ssma,'longsma':lsma})

    def get_signal(self):
        current_ssma = self.sma[0]['shortsma']
        current_lsma = self.sma[0]['longsma']
        last_ssma    = self.sma[1]['shortsma']
        last_lsma    = self.sma[1]['longsma']

        if (last_ssma > last_lsma) and (current_ssma <= current_lsma):
            return 'sell'
        elif (last_ssma < last_lsma) and (current_ssma >= current_lsma):
            return 'buy'
        else:
            return 'wait'
