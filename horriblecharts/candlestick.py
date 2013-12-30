from tkinter import *
from tkinter.ttk import *

STYLES = \
{'default':\
    {'background':'#121235',\
     'filled':'#ff3838',\
     'hollow':'#6dbc4a',\
     'shortsma':'#2bdbc6',\
     'longsma':'#db3c2b',\
     'shortema':'#1a7cf6',\
     'longema':'#f6df1a',\
     'donchian_channels':'#ffffff'\
    },\
 'dark_as_my_soul':\
    {'background':'#000000',\
     'filled':'#ff0000',\
     'hollow':'#48ff00',\
     'shortsma':'#00ffc0',\
     'longsma':'#f000ff',\
     'shortema':'#ffc0ff',\
     'longema':'#ff5a00',\
     'donchian_channels':'#ffffff'\
    }\
}

class Candlestick(object):
    def __init__(self,master,\
                 xspacing=10,\
                 zoom=30,\
                 candlewidth=10,\
                 datumsize=1000,\
                 datumrange=3000,\
                 tick=1,\
                 ):
        self.frame = Frame(master)
        self.frame.grid_rowconfigure(0,weight=1)
        self.frame.grid_columnconfigure(0,weight=1)

        self.xspacing = xspacing
        self.candlewidth = candlewidth
        self.zoom = zoom
        self.margin = 100

        self.width = self.margin + (datumsize* (candlewidth * xspacing))
        self.height = datumrange*zoom

        #scrollbars
        self.xscroll = Scrollbar(self.frame,orient=HORIZONTAL)
        self.yscroll = Scrollbar(self.frame,orient=VERTICAL)
        #create chart and connect scrollbars
        self.chart = Canvas(self.frame,\
                     scrollregion=(0,0,self.width,self.height),\
                     xscrollcommand=self.xscroll.set,\
                     yscrollcommand=self.yscroll.set,\
                     background=STYLES['default']['background'])

        self.xscroll.config(command=self.chart.xview)
        self.yscroll.config(command=self.chart.yview)
        
        self.chart.grid(row=0,column=0,sticky=N+S+E+W)
        self.yscroll.grid(row=0,column=1,sticky=N+S)
        self.xscroll.grid(row=1,column=0,sticky=E+W)

    def add_candles(self,datum):
        xoffset = self.width - self.margin
        yoffset = self.height
        self.candles = []
        style = STYLES['default']
        for data in datum:
             body = self.chart.create_rectangle(xoffset-self.candlewidth,
                                               yoffset-data['open']*self.zoom,\
                                               xoffset,\
                                               yoffset-data['close']*self.zoom,\
                                               fill = style['filled'])
             wick = self.chart.create_line(xoffset-(self.candlewidth/2),
                                               yoffset-data['high']*self.zoom,\
                                               xoffset-(self.candlewidth/2),\
                                               yoffset-data['low']*self.zoom,\
                                               fill = style['filled'])
             if data['close'] > data['open']:
                 self.chart.itemconfig(body,fill='',outline=style['hollow'])
                 self.chart.itemconfig(wick,fill=style['hollow'])

             self.candles.append({'body':body,'wick':wick})
             xoffset -= self.xspacing + self.candlewidth
        
        self.center_canvas()

    def center_canvas(self):
        coords = self.chart.coords(self.candles[0]['wick'])
        height = self.chart.winfo_height() / 2
        self.chart.yview_moveto(( (max([coords[1],coords[3]])) - height ) / self.height)
        self.chart.xview_moveto(1.0)

    def update_candles(self,last):
        remove = self.candles.pop()
        self.chart.delete(remove['wick'])
        self.chart.delete(remove['body'])

        for candle in self.candles:
            self.chart.move(candle['wick'],-self.xspacing-self.candlewidth,0)
            self.chart.move(candle['body'],-self.xspacing-self.candlewidth,0)
        
        xoffset = self.width-self.margin
        yoffset = self.height
        
        new_body = self.chart.create_rectangle(xoffset-self.candlewidth,
                                               yoffset-last['open']*self.zoom,\
                                               xoffset,\
                                               yoffset-last['close']*self.zoom,\
                                               fill = 'red')

        new_wick = self.chart.create_line(xoffset-(self.candlewidth/2),
                                           yoffset-last['high']*self.zoom,\
                                           xoffset-(self.candlewidth/2),\
                                           yoffset-last['low']*self.zoom,\
                                           fill = 'red')
        if last['close'] > last['open']:
            self.chart.itemconfig(new_body,fill='',outline='green')
            self.chart.itemconfig(new_wick,fill='green')

        self.candles.insert(0,{'body':new_body,'wick':new_wick})
        
        self.center_canvas()

    def add_sma(self,datum):
        xoffset = self.width-self.margin
        yoffset = self.height
        self.sma =[]        
        i = 0
        style = STYLES['default']
        while i < len(datum)-1:
            longsma = self.chart.create_line(xoffset-(self.candlewidth/2),
                                             yoffset-datum[i]['longsma']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-datum[i+1]['longsma']*self.zoom,\
                                             fill = style['longsma'])
            shortsma = self.chart.create_line(xoffset-(self.candlewidth/2),
                                              yoffset-datum[i]['shortsma']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-datum[i+1]['shortsma']*self.zoom,\
                                              fill =  style['shortsma'])
             
            self.sma.append({'shortsma':shortsma,'longsma':longsma})
            xoffset -= self.xspacing + self.candlewidth
    
            i += 1

    def add_ema(self,datum):
        xoffset = self.width-self.margin
        yoffset = self.height
        self.ema = []        
        i = 0
        style  = STYLES['default']
        while i < len(datum)-1:
            longema = self.chart.create_line(xoffset-(self.candlewidth/2),
                                             yoffset-datum[i]['longema']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-datum[i+1]['longema']*self.zoom,\
                                             fill = style['longema'])
            shortema = self.chart.create_line(xoffset-(self.candlewidth/2),
                                              yoffset-datum[i]['shortema']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-datum[i+1]['shortema']*self.zoom,\
                                              fill = style['shortema'])
             
            self.ema.append({'shortema':shortema,'longema':longema})
            xoffset -= self.xspacing + self.candlewidth
    
            i += 1

    def add_donchian_channels(self,datum):
        xoffset = self.width-self.margin
        yoffset = self.height
        self.donchian_channels = []        
        i = 0
        style = STYLES['default']
        while i < len(datum)-1:
            upper = self.chart.create_line(xoffset-(self.candlewidth/2),
                                             yoffset-datum[i]['upper']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-datum[i+1]['upper']*self.zoom,\
                                             fill = style['donchian_channels'])
            lower = self.chart.create_line(xoffset-(self.candlewidth/2),
                                              yoffset-datum[i]['lower']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-datum[i+1]['lower']*self.zoom,\
                                              fill = style['donchian_channels'])
             
            self.donchian_channels.append({'upper':upper,'lower':lower})
            xoffset -= self.xspacing + self.candlewidth
    
            i += 1


    def update_sma(self,last):
        remove = self.sma.pop()
        self.chart.delete(remove['shortsma'])
        self.chart.delete(remove['longsma'])

        for sma in self.sma:
            self.chart.move(sma['shortsma'],-self.xspacing-self.candlewidth,0)
            self.chart.move(sma['longsma'],-self.xspacing-self.candlewidth,0)
        
        xoffset = self.width-self.margin
        yoffset = self.height
        
        style = STYLES['default']

        new_longsma = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                             yoffset-last[0]['longsma']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-last[1]['longsma']*self.zoom,\
                                             fill = style['longsma'])

        new_shortsma = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                              yoffset-last[0]['shortsma']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-last[1]['shortsma']*self.zoom,\
                                              fill =  style['shortsma'])
             
        
        self.sma.insert(0,{'shortsma':new_shortsma,'longsma':new_longsma})
        

    def update_ema(self,last):
        remove = self.ema.pop()
        self.chart.delete(remove['shortema'])
        self.chart.delete(remove['longema'])

        for ema in self.ema:
            self.chart.move(ema['shortema'],-self.xspacing-self.candlewidth,0)
            self.chart.move(ema['longema'],-self.xspacing-self.candlewidth,0)
        
        xoffset = self.width-self.margin
        yoffset = self.height
        
        style = STYLES['default']

        new_longema = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                             yoffset-last[0]['longema']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-last[1]['longema']*self.zoom,\
                                             fill = style['longema'])

        new_shortema = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                              yoffset-last[0]['shortema']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-last[1]['shortema']*self.zoom,\
                                              fill =  style['shortema'])
             
        
        self.ema.insert(0,{'shortema':new_shortema,'longema':new_longema})
        
    def update_donchian_channels(self,last):
        remove = self.donchian_channels.pop()
        self.chart.delete(remove['upper'])
        self.chart.delete(remove['lower'])

        for channel in self.donchian_channels:
            self.chart.move(channel['upper'],-self.xspacing-self.candlewidth,0)
            self.chart.move(channel['lower'],-self.xspacing-self.candlewidth,0)
        
        xoffset = self.width-self.margin
        yoffset = self.height
        
        style = STYLES['default']

        new_upper = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                             yoffset-last[0]['upper']*self.zoom,\
                                             xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                             yoffset-last[1]['upper']*self.zoom,\
                                             fill = style['donchian_channels'])

        new_lower = self.chart.create_line(xoffset-(self.candlewidth/2),\
                                              yoffset-last[0]['lower']*self.zoom,\
                                              xoffset-(1.5*self.candlewidth)-self.xspacing,\
                                              yoffset-last[1]['lower']*self.zoom,\
                                              fill =  style['donchian_channels'])
             
        
        self.donchian_channels.insert(0,{'upper':new_upper,'lower':new_lower})
        
