import time
import datetime
import sys
import aggregator as yat

####################
option = yat.Clipars(sys.argv[1:])
####################

logger = yat.CustomLogger.setup_custom_logger(name='TickerFetcher', log_level='DEBUG')

symbol = "BTC/USDT"

def main():
    try:
        curtick = 0
        ask_data, bid_data = [], []
        exc = getattr(yat, option.exchange.title())
        exc.loadexchange()
        dbclient = yat.Influx('YAT')

        while True:
            if option.fetchtype.lower() == 'ticker':
                exc.fetchtickers()
                dbclient.writepoints(exc.curtickers)

            if option.fetchtype.lower() == 'derivative':
                exc.fetchderivatives()
                dbclient.writepoints(exc.curderivatives)

            if option.fetchtype.lower() == 'tickmas':
                MA1 = 100
                MA2 = 50
                MA3 = 20
                MA4 = 10
                window = 100
                ticker = exc.ex.fetch_ticker(symbol)
                ask_data.append(ticker['ask'])
                bid_data.append(ticker['bid'])
                if len(ask_data) > window+1:
                    del ask_data[0]
                    ema1_ask = yat.computeEMA(ask_data, MA1)
                    ema2_ask = yat.computeEMA(ask_data, MA2)
                    ema3_ask = yat.computeEMA(ask_data, MA3)
                    ema4_ask = yat.computeEMA(ask_data, MA4)
                    del bid_data[0]
                    ema1_bid = yat.computeEMA(bid_data, MA1)
                    ema2_bid = yat.computeEMA(bid_data, MA2)
                    ema3_bid = yat.computeEMA(bid_data, MA3)
                    ema4_bid = yat.computeEMA(bid_data, MA4)
                    updtmsg = dict()
                    updtlist = list()
                    updtmsg["measurement"] = "ticker_mas"
                    updtmsg["tags"] = {"ticker": symbol, "exchange": option.exchange.lower()}
                    updtmsg["fields"] = dict()
                    updtmsg["fields"]['ema100ask'] = ema1_ask[-1]
                    updtmsg["fields"]['ema50ask'] = ema2_ask[-1]
                    updtmsg["fields"]['ema20ask'] = ema3_ask[-1]
                    updtmsg["fields"]['ema10ask'] = ema4_ask[-1]
                    updtmsg["fields"]['ema100bid'] = ema1_bid[-1]
                    updtmsg["fields"]['ema50bid'] = ema2_bid[-1]
                    updtmsg["fields"]['ema20bid'] = ema3_bid[-1]
                    updtmsg["fields"]['ema10bid'] = ema4_bid[-1]
                    updtlist.append(updtmsg)
                    # save to db
                    dbclient.writepoints(updtlist)

            if option.fetchtype.lower() == 'ohlcvind':
                ohlcv = exc.fetchohlcv(symbol, frame='1m')
                date = [x[0] for x in ohlcv]
                closep = [x[4] for x in ohlcv]
                # highp = [x[2] for x in ohlcv]
                # lowp = [x[3] for x in ohlcv]
                # openp = [x[1] for x in ohlcv]
                # volume = [x[5] for x in ohlcv]

                rsi = yat.computeRSI(closep, n=14)
                macd, emaslow, emafast = yat.computeMACD(closep, slow=26, fast=12)

                updtmsg = dict()
                updtlist = list()
                updtmsg["measurement"] = "ohlcvind"
                updtmsg["tags"] = {"ticker": symbol, "exchange": option.exchange.lower()}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['rsi14_1'] = rsi[-1]
                updtmsg["fields"]['ema12_1'] = emafast[-1]
                updtmsg["fields"]['ema26_1'] = emaslow[-1]
                updtmsg["fields"]['macd12_26_1'] = macd[-1]

                updtlist.append(updtmsg)

                dbclient.writepoints(updtlist)

            msg1 = "#%s %s InfluxDB updated %s from %s" % (curtick,
                                                           datetime.datetime.now(),
                                                           option.fetchtype.lower(),
                                                           option.exchange.lower())
            logger.info(msg1)
            curtick = curtick + 1
            time.sleep(option.pause)

    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

if __name__ == '__main__':
    main()
