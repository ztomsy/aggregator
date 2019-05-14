import time
import datetime
import sys
import tkg_interfaces as TKG



####################
option = TKG.Clipars(sys.argv[1:])
####################

# Init logger and define log_level verbosity
logger = TKG.CustomLogger.setup_custom_logger(name='TickerFetcher', log_level='DEBUG')

# define symbol for tickmas and ohlcvind(TODO Convert to parameter)
symbol = "BTC/USDT"

def main():
    try:
        # define counter
        curtick = 0
        # Initialize data collecting for ask and bid to count mas
        ask_data, bid_data = [], []
        # initialise necessary exchange class constructor(TODO convert to attr function)
        if option.exchange.lower() == 'kucoin':
            exc = TKG.Kucoin()
        if option.exchange.lower() == 'binance':
            exc = TKG.Binance(logger)
        if option.exchange.lower() == 'kraken':
            exc = TKG.Kraken()
        if option.exchange.lower() == 'poloniex':
            exc = TKG.Poloniex()
        if option.exchange.lower() == 'bittrex':
            exc = TKG.Bittrex()
        # load exchange
        exc.loadexchange()
        # initialise database class with name
        dbclient = TKG.Influx('YAT')

        while True:
            # Load and write to DB different data, defined as argument
            if option.fetchtype.lower() == 'ticker':
                # load tickers
                exc.fetchtickers()
                # save to db
                dbclient.writepoints(exc.curtickers)

            if option.fetchtype.lower() == 'derivative':
                # load derivative data
                exc.fetchderivatives()
                # write derivatives to db
                dbclient.writepoints(exc.curderivatives)

            if option.fetchtype.lower() == 'tickmas':
                # define mas
                MA1 = 100
                MA2 = 50
                MA3 = 20
                MA4 = 10
                window = 100
                # write mas data to db
                ticker = exc.ex.fetch_ticker(symbol)
                ask_data.append(ticker['ask'])
                bid_data.append(ticker['bid'])
                if len(ask_data) > window+1:
                    del ask_data[0]
                    ema1_ask = TKG.computeEMA(ask_data, MA1)
                    ema2_ask = TKG.computeEMA(ask_data, MA2)
                    ema3_ask = TKG.computeEMA(ask_data, MA3)
                    ema4_ask = TKG.computeEMA(ask_data, MA4)
                    del bid_data[0]
                    ema1_bid = TKG.computeEMA(bid_data, MA1)
                    ema2_bid = TKG.computeEMA(bid_data, MA2)
                    ema3_bid = TKG.computeEMA(bid_data, MA3)
                    ema4_bid = TKG.computeEMA(bid_data, MA4)
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
                # load ohlcv 1 min candles
                ohlcv = exc.fetchohlcv(symbol, frame='1m')
                date = [x[0] for x in ohlcv]
                closep = [x[4] for x in ohlcv]
                # highp = [x[2] for x in ohlcv]
                # lowp = [x[3] for x in ohlcv]
                # openp = [x[1] for x in ohlcv]
                # volume = [x[5] for x in ohlcv]

                # Calculate RSI
                rsi = TKG.computeRSI(closep, n=14)

                # Compute MACD (Divergence between 2 ma)
                # and count ema of macd for fun
                # nema = 9
                macd, emaslow, emafast = TKG.computeMACD(closep, slow=26, fast=12)
                # ema9 = TKG.computeEMA(macd, nema)
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
                # save to db
                dbclient.writepoints(updtlist)

            # if option.fetchtype.lower() == 'ob':
            #     # load exchange
            #     exc.loadexchange()
            #     # load ob
            #     exc.fetchob(symbol)
            #     updtlist = list()
            #     # prepare ask update message
            #     askupdtmsg = dict()
            #     askupdtmsg["measurement"] = symbol
            #     askupdtmsg["tags"] = {"side": "ask", "exchange": option.exchange.lower()}
            #     askupdtmsg["fields"] = exc.ob._ask_book
            #     updtlist.append(askupdtmsg)
            #     # prepare bid update message
            #     bidupdtmsg = dict()
            #     bidupdtmsg["measurement"] = symbol
            #     bidupdtmsg["tags"] = {"side": "bid", "exchange": option.exchange.lower()}
            #     bidupdtmsg["fields"] = exc.ob._bid_book
            #     updtlist.append(bidupdtmsg)
            #     # save to db
            #     dbclient.writepoints(updtlist)

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