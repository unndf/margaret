class Trailingstop(object):
    def __init__(self,initial_price,percentage):
        self.step = 0.01 * percentage
        self.stop = initial_price - self.step

    def update(self,last):
        stop = last - (self.step)
        if stop >= self.stop:
            self.stop = stop
