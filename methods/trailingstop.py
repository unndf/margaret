class Trailingstop(object):
    def __init__(self,percentage):
        self.percentage = 0.01 * percentage
        self.stoploss = 0

    def update(last):
        stop = last - (last*self.percentage)
        if stop >= self.stoploss:
            self.stoploss = stop
