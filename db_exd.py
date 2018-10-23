import time
import datetime
import sys
import tkg_interfaces as TKG


####################
option = TKG.Clipars(sys.argv[1:])
####################


def main():
    try:
        # define counter
        curtick = 0
        # initialise necesseray exchange class constructor
        if option.exchange.lower() == 'kucoin':
            exc = TKG.Kucoin()
        if option.exchange.lower() == 'binance':
            exc = TKG.Binance()
        if option.exchange.lower() == 'kraken':
            exc = TKG.Kraken()
        if option.exchange.lower() == 'poloniex':
            exc = TKG.Poloniex()
        if option.exchange.lower() == 'bittrex':
            exc = TKG.Bittrex()
        # initialise database class
        dbclient = TKG.Influx()
        # load exchange
        # todo catch exc load errors
        exc.loadexchange()
        while True:
            '''Load and write to DB different data, defined as argument'''
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
            if option.fetchtype.lower() == 'splitticker':    
                # Alternative variant to use another db structure with 
                # single value per ticker
                # load tickers
                exc.splittickers()
                # save to db
                dbclient.writepoints(exc.newtickers)
            # if option.fetchtype.lower() == 'balances': 
                # write balance data to db
                # exc.myBalance()
                # save to db
                # dbclient.writepoints(exc.mybalances)
            curtick = curtick + 1
            msg1 = "#%s %s InfluxDB updated %s from %s" % (curtick, 
                                                        datetime.datetime.now(),
                                                        option.fetchtype.lower(),
                                                        option.exchange.lower())
            print(msg1)
            time.sleep(option.pause)

    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

if __name__ == '__main__':
    main()