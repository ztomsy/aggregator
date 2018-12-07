import tkg_interfaces as TKG
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
import time

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
# todo catch exc load errors
exc.loadexchange()

def data_gen(exc):
    cnt = 0
    while cnt < 10:
        cnt+=1
        # Fetch ticker in update thread
        time.sleep(0.5)
        ticker = exc.ex.fetch_ticker(symbol)
        t = ticker['timestamp']
        y1 = ticker['bid']
        y2 = ticker['ask']
        # adapted the data generator to yield both sin and cos
        yield t, y1, y2


# create a figure with two subplots
figure, (ax1, ax2) = pyplot.subplots(2, 1)
# make a little extra space between the subplots
figure.subplots_adjust(hspace=0.5)

# intialize two line objects (one in each axes)
line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2, color='r')
line = [line1, line2]

# the same axes initalizations as before (just now we do it for both of them)
for ax in [ax1, ax2]:
    # ax.set_ylim(-1.1, 1.1)
    # ax.set_xlim(0, 5)
    ax.grid()

# initialize the data arrays
tdata, biddata, askdata = [], [], []

def run(data):
    # update the data
    t, y1, y2 = data
    tdata.append(t)
    biddata.append(y1)
    askdata.append(y2)

    # axis limits checking. Same as before, just for both axes
    for ax in [ax1, ax2]:
        xmin, xmax = ax.get_xlim()
        if t >= xmax:
            # ax.set_xlim(xmin, 2*xmax)
            ax.figure.canvas.draw()

    # update the data of both line objects
    line[0].set_data(tdata, biddata)
    line[1].set_data(tdata, askdata)

    return line

ani = FuncAnimation(figure, run, data_gen(exc), blit=True, interval=500,
                    repeat=False)
pyplot.show()

#figure = pyplot.figure()

# Create 2 plots
# figure, (ax1, ax2) = pyplot.subplots(2, 1, sharex=True, figsize=(15, 10))
# make a little extra space between the subplots
# figure.subplots_adjust(hspace=0.5)

# initialize line to plots
# bid_line, = ax1.plot_date(bid_t_data, bid_data, '-')
# ask_line, = ax2.plot_date(ask_t_data, ask_data, '-')
# line = [bid_line, ask_line]

# def update(frame):
#     # Fetch ticker in update thread
#     ticker = exc.ex.fetch_ticker(symbol)
#
#     bid_t_data.append(datetime.now())
#     bid_data.append(ticker['bid'])
#     if len(bid_data)>200:
#         del bid_data[0]
#         del bid_t_data[0]
#
#     line[0].set_data(bid_t_data, bid_data)
#
#     ask_t_data.append(datetime.now())
#     ask_data.append(ticker['ask'])
#     if len(ask_data) > 200:
#         del ask_data[0]
#         del ask_t_data[0]
#
#     line[1].set_data(bid_t_data, bid_data)
#
#     figure.gca().relim()
#     figure.gca().autoscale_view()
#     return line,
#
# animation = FuncAnimation(figure, update, interval=100)
#
# pyplot.show()


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

