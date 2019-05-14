import tkg_interfaces as TKG
import time
from datetime import datetime
from matplotlib import pyplot as plt

def main():
    try:
        # define counter
        curtick = 0
        # define symbol
        symbol = "BTC/USDT"
        MA1 = 10
        MA2 = 20
        # initialise necesseray exchange class constructor
        exc = TKG.Binance()
        # initialise database class
        dbclient = TKG.Influx()
        # load exchange
        # todo catch exc load errors
        exc.loadexchange()
        while True:
            ohlcv = exc.fetchohlcv(symbol)

            # datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            # date = [datetime.utcfromtimestamp(x[0]/1000).strftime("%m/%d") for x in ohlcv]
            date = [x[0] for x in ohlcv]
            closep = [x[4] for x in ohlcv]
            highp = [x[2] for x in ohlcv]
            lowp = [x[3] for x in ohlcv]
            openp = [x[1] for x in ohlcv]
            volume = [x[5] for x in ohlcv]

            # Calculate few ma's
            Av1 = TKG.computeMA(closep, MA1)
            Av2 = TKG.computeMA(closep, MA2)

            # Calculate RSI
            rsi = TKG.computeRSI(closep, n=14)

            # Compute MACD (Divergence between 2 ma)
            # and count ema of macd for fun
            nema = 9
            macd, emaslow, emafast = TKG.computeMACD(closep, slow=26, fast=12)
            ema9 = TKG.computeEMA(macd, nema)

            # Plot everything by leveraging the matplotlib package
            # fig, ax = plt.subplots(figsize=(16, 9))

            # Create 3 plots
            fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, figsize=(15, 10))
            # make a little extra space between the subplots
            fig.subplots_adjust(hspace=0.5)

            ax1.plot(date, closep, label=symbol)
            ax1.plot(date[MA1 - 1:], Av1, label='MA 10')
            ax1.plot(date[MA2 - 1:], Av2, label='MA 20')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Adjusted closing price')
            ax1.grid(True)
            # ax1.legend()

            ax2.plot(date, rsi, label='RSI 14')
            ax2.set_xlabel('Date')
            ax2.set_ylabel('RSI 14')
            ax2.grid(True)
            # ax2.legend()

            ax3.plot(date, macd, label='MACD 12-26')
            ax3.plot(date, ema9, label='MACD ema9')
            ax3.set_xlabel('Date')
            ax3.set_ylabel('MACD 12-26')
            ax3.grid(True)

            # ax4.plot(date, macd, label='MACD 12-26')
            # ax4.set_xlabel('Date')
            # ax4.set_ylabel('MACD 12-26')
            # ax4.grid(True)



            fig.tight_layout()

            plt.show()

            x = 0
            y = len(date)
            newAr = []
            while x < y:
                appendLine = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
                newAr.append(appendLine)
                x += 1

            SP = len(date[MA2 - 1:])

            rsi = TKG.computeRSI(closep)


    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

if __name__ == '__main__':
    main()