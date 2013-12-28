from time import sleep

class Backoff(object):
    def __init__(self,factor=2):
        self.time = 0
        self.factor = factor

    def sleep(self):
        if self.time == 0:
            self.time = 1
        else:
            sleep(self.time)
            self.time *= self.factor
