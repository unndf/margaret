from tkinter import *
from tkinter.ttk import *
from copy import deepcopy

class Candlestick(object):
    def __init__(self,master,xspacing=10,zoom=10,candlewidth=5,datumsize=1000, datumrange=3000,tick=1,margin=100):
        self.frame = Frame(master)
        self.frame.grid_rowconfigure(0,weight=1)
#        self.frame.grid_rowconfigure(1,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)
 #       self.frame.grid_columnconfigure(1,weight=1)

        self.xspacing = xspacing
        self.zoom     = zoom
        self.candlewidth = candlewidth
        self.margin = margin
        self.width  = candlewidth*datumsize + (datumsize+1)*xspacing + margin
        self.height = datumrange*zoom
        self.datumsize = datumsize
        self.candles = []
        self.sma = []
        self.datum_old = []
        self.xscroll = Scrollbar(self.frame,orient=HORIZONTAL)
        self.yscroll = Scrollbar(self.frame,orient=VERTICAL)
        self.chart = Canvas(self.frame,scrollregion=(0,0,self.width,self.height), xscrollcommand=self.xscroll.set,yscrollcommand=self.yscroll.set)
        self.chart.configure(background='black')
        self.xscroll.config(command=self.chart.xview)
        self.yscroll.config(command=self.chart.yview)
        
        self.chart.grid(row=0,column=0,sticky=N+S+E+W)
        self.yscroll.grid(row=0,column=1,sticky=N+S)
        self.xscroll.grid(row=1,column=0,stick=E+W)
        self.sar=[]

        self.generate_candles()
        self.generate_sar()
        self.generate_sma()
        self.create_ticks()
    
    def update_sma(self,datum):
        if datum != self.datum_old:
            for pair in self.sma:
                ashort = pair['short']
                along = pair['long']
                self.chart.move(ashort,-1*(self.xspacing+self.candlewidth),0)
                self.chart.move(along,-1*(self.xspacing+self.candlewidth),0)
            
            self.sma.pop(0)
            
            xoffset=  self.datumsize*(self.xspacing+self.candlewidth)-self.candlewidth
            yoffset = self.height
            new_short = self.chart.create_line(xoffset+self.candlewidth//2,\
                                            yoffset-(datum[0]['s_sma']*self.zoom),\
                                            (xoffset-self.candlewidth//2)-self.xspacing,\
                                            yoffset-(datum[1]['s_sma']*self.zoom),\
                                            fill="magenta"\
                                            )
            new_long = self.chart.create_line(xoffset+self.candlewidth//2,\
                                            yoffset-(datum[0]['l_sma']*self.zoom),\
                                            (xoffset-self.candlewidth//2)-self.xspacing,\
                                            yoffset-(datum[1]['l_sma']*self.zoom),\
                                            fill="cyan"\
                                            )
            self.sma.append({'short':new_short,'long':new_long})
            self.datum_old=deepcopy(datum)
           
    def update(self,datum):
        if datum != self.datum_old:
            for candle in self.candles:
                body = candle['body']
                wick = candle['wick']
                
                self.chart.move(body,-1*(self.xspacing+self.candlewidth),0)
                self.chart.move(wick,-1*(self.xspacing+self.candlewidth),0)
            
            self.candles.pop(0)
            
            xoffset= self.xspacing + self.datumsize*(self.xspacing+self.candlewidth)
            yoffset = self.height

            new_body = self.chart.create_rectangle(xoffset,\
                                            yoffset-(datum[0]['open']*self.zoom),\
                                            xoffset+self.candlewidth,\
                                            yoffset-(datum[0]['close']*self.zoom),\
                                            outline="red",\
                                            fill="red"\
                                            )
     
            new_wick = self.chart.create_line(xoffset+self.candlewidth//2,\
                                       yoffset-1-(datum[0]['high']*self.zoom),\
                                       xoffset+self.candlewidth//2,\
                                       yoffset-1-(datum[0]['low']*self.zoom),\
                                       fill="red"\
                                       )
            
            if datum[0]['open'] <= datum[0]['close']:
                self.chart.itemconfig(new_body,outline="green",fill="")
                self.chart.itemconfig(new_wick,fill="green")
            
            self.candles.append({'body':new_body,'wick':new_wick})
            self.update_sma(datum)

            self.datum_old=deepcopy(datum)
            self.update_sar(datum)    
    
    def create_ticks(self):
        xoffset=self.width-(self.margin)
        yoffset=self.height-(self.zoom)
        i = 1
        while yoffset > 0:
            self.chart.create_text(xoffset+self.margin//2,yoffset,text=i,fill='white')
            i+=1
            yoffset-=self.zoom*1

    def generate_sma(self):
        i = self.datumsize -1
        xoffset = self.xspacing
        yoffset = self.height
        while i >= 0:
            new_short = self.chart.create_line(xoffset+self.candlewidth//2,\
                                            yoffset-(1*self.zoom),\
                                            (xoffset-self.candlewidth//2)-self.xspacing,\
                                            yoffset-(1*self.zoom),\
                                            fill="magenta"\
                                            )
            new_long = self.chart.create_line(xoffset+self.candlewidth//2,\
                                            yoffset-(1*self.zoom),\
                                            (xoffset-self.candlewidth//2)-self.xspacing,\
                                            yoffset-(1*self.zoom),\
                                            fill="cyan"\
                                            )
            
            self.sma.append({'short':new_short,'long':new_long})
            
            i-=1
            xoffset += self.xspacing + self.candlewidth
    
    def generate_candles(self):
        i = self.datumsize -1
        xoffset = self.xspacing
        yoffset = self.height
        while i >= 0:
            body = self.chart.create_rectangle(xoffset,\
                                    yoffset-(1*self.zoom),\
                                    xoffset+self.candlewidth,\
                                    yoffset-(1*self.zoom),\
                                    outline="red",\
                                    fill="red"\
                                    )
            wick = self.chart.create_line(xoffset+self.candlewidth//2,\
                                   yoffset-(1*self.zoom),\
                                   xoffset+self.candlewidth//2,\
                                   yoffset-(1*self.zoom),\
                                   fill="red"\
                                   )
            self.candles.append({'body':body,'wick':wick})
            
            i-=1
            xoffset += self.xspacing + self.candlewidth

    def generate_sar(self):
        i = self.datumsize -1
        xoffset = self.xspacing
        yoffset = self.height
        while i >= 0:
            point = self.chart.create_oval((xoffset+self.candlewidth//2)-2,\
                                   (yoffset-(1*self.zoom))-2,\
                                   (xoffset+self.candlewidth//2)+2,\
                                   (yoffset-(1*self.zoom))+2,\
                                   outline="white",\
                                   fill  = "orange"\
                                   )
            self.sar.append({'sar':point})
            print(str(point))
            i-=1
            xoffset += self.xspacing + self.candlewidth
        

    def update_sar(self,datum):
            for point in self.sar:
                self.chart.move(point['sar'],-1*(self.xspacing+self.candlewidth),0)
            
            self.sar.pop(0)
            
            xoffset=  self.datumsize*(self.xspacing+self.candlewidth)-self.candlewidth
            yoffset = self.height
            new_point = self.chart.create_oval((xoffset+self.candlewidth//2)-2,\
                                            (yoffset-(datum[0]['stoploss']*self.zoom))-2,\
                                            (xoffset+self.candlewidth//2)+2,\
                                            (yoffset-(datum[0]['stoploss']*self.zoom)+2),\
                                            fill="orange",\
                                            outline="white"\
                                            )
            self.sar.append({'sar':new_point})
 
            print(self.height-self.datum_old[0]['stoploss'])
        
