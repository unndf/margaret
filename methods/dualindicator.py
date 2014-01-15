class Dualindicator(object):
    def __init__(self,primary,secondary,limit=3):
        self.primary = primary
        self.secondary = secondary
        self.primary_stack = ["wait"] * limit
        self.secondary_stack = ["wait"] * limit
        self.limit = limit
        
    def update(self,datum):
        self.primary.update(datum)
        self.secondary.update(datum)

    def get_signal(self):
        primary_signal = self.primary.get_signal()
        secondary_signal = self.secondary.get_signal()
        
        self.primary_stack.pop()
        self.secondary_stack.pop()
        self.primary_stack.insert(0,primary_signal)
        self.secondary_stack.insert(0,secondary_signal)

        if ('buy' in self.primary_stack) and ('buy' in self.secondary_stack):
            self.primary_stack = ["wait"] * self.limit
            self.secondary_stack = ["wait"] * self.limit
            return 'buy'

        elif ('sell' in self.primary_stack) and ('sell' in self.secondary_stack):
            self.primary_stack = ["wait"] * self.limit
            self.secondary_stack = ["wait"] * self.limit
            return 'sell'
        
        else:
            return 'wait'
