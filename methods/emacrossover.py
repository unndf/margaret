class EMAcrossover(object):
    def __init__(self,trading_periods,shortema=7,longema=30,coefficient=0.2):
        self.shortema = shortema
        self.longema  = longema
        self.coefficient = 1-coefficient
        self.ema = []

        #calculate the ema for the trading periods already given
        i = 0
        while i < (len(trading_periods)) - longema:
            raw = trading_periods[i:i+longema-1]
            prices = []
            for price in raw:
                prices.append(price['close'])

            lema = self.calc_ema(prices)
            sema = self.calc_ema(prices[:shortema-1])

            self.ema.append({'shortema':sema,'longema':lema})
            i+=1

    def calc_ema(self,prices):
        total = 0
        coeff = 1
        for price in prices:
            total += price * coeff
            coeff *= self.coefficient

        coeff = 1
        denom = 0
        for i in range(len(prices)):
            denom += coeff
            coeff *= self.coefficient

        return total/denom
    
    #last periods must be the length of the longema period
    def update(self,last_periods):
        prices = []
        for price in last_periods:
            prices.append(price['close'])

        prices = prices[:self.longema-1]
        sema = self.calc_ema(prices)
        lema = self.calc_ema(prices[:self.shortema-1])

        self.ema.pop()
        self.ema.insert(0,{'shortema':sema,'longema':lema})

    def get_signal(self):
        current_sema = self.ema[0]['shortema']
        current_lema = self.ema[0]['longema']
        last_sema    = self.ema[1]['shortema']
        last_lema    = self.ema[1]['longema']

        if (last_sema > last_lema) and (current_sema <= current_lema):
            return 'sell'
        elif (last_sema < last_lema) and (current_sema >= current_lema):
            return 'buy'
        else:
            return 'wait'
