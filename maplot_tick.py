import tkg_interfaces as TKG
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
import time

# time_format = '%Y-%m-%d %H:%M:%S'

# define counter
curtick = 0
# define symbol
symbol = "BTC/USDT"
MA1 = 10
MA2 = 20
# initialise exchange class constructor
exc = TKG.Binance()
# initialise database class
# dbclient = TKG.Influx()
# load exchange
exc.loadexchange()

# Initialize data collecting
bid_data, bid_t_data = [], []
#ask_data, ask_t_data = [], []

figure = pyplot.figure()

# # Create 2 plots
# figure, (ax1, ax2) = pyplot.subplots(2, 1, sharex=True, figsize=(15, 10))
# # make a little extra space between the subplots
# figure.subplots_adjust(hspace=0.5)

bid_line, = pyplot.plot_date(bid_t_data, bid_data, '-')

# initialize line to plots
# bid_line, = ax1.plot_date(bid_t_data, bid_data, '-')
# ask_line, = ax2.plot_date(ask_t_data, ask_data, '-')
# line = [bid_line, ask_line]

def update(frame):
    # Fetch ticker in update thread
    ticker = exc.ex.fetch_ticker(symbol)
    # time = datetime.strptime(datetime.date, time_format)
    bid_t_data.append(datetime.now())
    bid_data.append(ticker['bid'])
    if len(bid_data)>10:
        del bid_data[0]
        del bid_t_data[0]

    bid_line.set_data(bid_t_data, bid_data)

    # ask_t_data.append(datetime.now())
    # ask_data.append(ticker['ask'])
    # if len(ask_data) > 200:
    #     del ask_data[0]
    #     del ask_t_data[0]
    #
    # line[1].set_data(bid_t_data, bid_data)
    #
    figure.gca().relim()
    figure.gca().autoscale_view()
    return bid_line,

animation = FuncAnimation(figure, update, interval=100)

pyplot.show()


# ohlcv = exc.fetchohlcv(symbol)
#
# # datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
# # date = [datetime.utcfromtimestamp(x[0]/1000).strftime("%m/%d") for x in ohlcv]
# date = [x[0] for x in ohlcv]
# closep = [x[4] for x in ohlcv]
# highp = [x[2] for x in ohlcv]
# lowp = [x[3] for x in ohlcv]
# openp = [x[1] for x in ohlcv]
# volume = [x[5] for x in ohlcv]
#
# # Calculate few ma's
# Av1 = TKG.computeMA(closep, MA1)
# Av2 = TKG.computeMA(closep, MA2)
#
# # Calculate RSI
# rsi = TKG.computeRSI(closep, n=14)
#
# # Compute MACD (Divergence between 2 ma)
# # and count ema of macd for fun
# nema = 9
# macd, emaslow, emafast = TKG.computeMACD(closep, slow=26, fast=12)
# ema9 = TKG.computeEMA(macd, nema)
#
# # Plot everything by leveraging the matplotlib package
# # figure, ax = plt.subplots(figsize=(16, 9))
#
# # Create 3 plots
# figure, (ax1, ax2, ax3) = pyplot.subplots(3, sharex=True, figsize=(15, 10))
# # make a little extra space between the subplots
# figure.subplots_adjust(hspace=0.5)
#
# ax1.plot(date, closep, label=symbol)
# ax1.plot(date[MA1 - 1:], Av1, label='MA 10')
# ax1.plot(date[MA2 - 1:], Av2, label='MA 20')
# ax1.set_xlabel('Date')
# ax1.set_ylabel('Adjusted closing price')
# ax1.grid(True)
# # ax1.legend()
#
# ax2.plot(date, rsi, label='RSI 14')
# ax2.set_xlabel('Date')
# ax2.set_ylabel('RSI 14')
# ax2.grid(True)
# # ax2.legend()
#
# ax3.plot(date, macd, label='MACD 12-26')
# ax3.plot(date, ema9, label='MACD ema9')
# ax3.set_xlabel('Date')
# ax3.set_ylabel('MACD 12-26')
# ax3.grid(True)
#
#
# figure.tight_layout()
#
# pyplot.show()

