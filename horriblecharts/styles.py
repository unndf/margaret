#These are the styles used in the candlestick chart

#background -> canvas background
#secondary_background -> fill color used for the ticks on the chart
#foreground -> used for foreground objects ie. text
#filled -> fill color used for filled (bearish) candles
#hollow -> fill color used for hollow (bullish) candles
#shortsma -> fill for short-term sma
#longsma -> fill for long term sma
#shortema -> fill used for short-term ema
#longema -> fill used for long-term ema
#donchian_channels -> fill used for the dochian channel indicator

STYLES = \
{'default':\
    {'background':'#fffbed',\
     'secondary_background':'#363636',\
     'foreground':'#000000',\
     'filled':'#ff3838',\
     'hollow':'#6dbc4a',\
     'shortsma':'#2bdbc6',\
     'longsma':'#db3c2b',\
     'shortema':'#1a7cf6',\
     'longema':'#f6df1a',\
     'donchian_channels':'#000000'\
    },\
 'dark_as_my_soul':\
    {'background':'#000000',\
     'secondary_background':'#363636',\
     'foreground':'#ffffff',\
     'filled':'#ff0000',\
     'hollow':'#48ff00',\
     'shortsma':'#00ffc0',\
     'longsma':'#f000ff',\
     'shortema':'#ffc0ff',\
     'longema':'#ff5a00',\
     'donchian_channels':'#ffffff'\
    }\
}
