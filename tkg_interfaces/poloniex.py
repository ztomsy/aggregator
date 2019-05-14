import ccxt
import sys
from .exconfig import Settings

class Poloniex:

    ex = ...  # type: ccxt.base

    def __init__(self):
        self.curtickers = []
        self.newtickers = []

    # Load exchange
    def loadexchange(self):

        try:
            self.ex = ccxt.poloniex({"apiKey": Settings.poloniex1ApiKey, "secret": Settings.poloniex1Sec})
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('Initialising poloniex: ', type(e).__name__, "!!!", e.args, ' ')
            # sys.exit()

    # Fetch exchanges tickers and wrap it into updtlist
    def fetchtickers(self):
        try:
            exFetT = self.ex.fetch_tickers()
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('While fetching tickers next error occur: ', type(e).__name__, "!!!", e.args)
            print("Exiting")
            sys.exit()
        # Wrap raw ticker data from ccxt into list of necessary dicts
        # ticker_data, ticker=<symbol>,exchange=<exchange> bid=1,ask=10,last=17

        # define new return dict and list
        updtlist = []

        for symbol in exFetT:
            if exFetT[symbol]['bid'] is not None:
                updtmsg = {}
                updtmsg["measurement"] = "ticker_data"
                updtmsg["tags"] = {"ticker": symbol, "exchange": "poloniex"}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['bid'] = exFetT[symbol]['bid']
                updtmsg["fields"]['ask'] = exFetT[symbol]['ask']
                updtmsg["fields"]['last'] = exFetT[symbol]['last']
                updtlist.append(updtmsg)

        self.curtickers = updtlist

    def splittickers(self):
        # Fetch exchanges ticker for necessary pair
        try:
            exFetT = self.ex.fetch_tickers()
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('While fetching tickers next error occur: ', type(e).__name__, "!!!", e.args)
            print("Exiting")
            sys.exit()

        # Wrap raw ticker data from ccxt into list of necessary dicts
        # bid, ticker=<symbol>,exchange=<exchange> value=0.0758659
        # ask, ticker=<symbol>,exchange=<exchange> value=0.0758654
        # last, ticker=<symbol>,exchange=<exchange> value=0.0758655
        # volume24, ticker=<symbol>,exchange=<exchange> value=100.256354
        # exts, ticker=<symbol>,exchange=<exchange> value=  exchange timestamp


        # define new return dict and list
        updtlist = []
        # define measurement list
        measurementlist = ['bid', 'ask', 'last']

        for symbol in exFetT:
            for ml in measurementlist:
                if exFetT[symbol][ml] is not None:
                    updtmsg = {}
                    updtmsg["measurement"] = ml
                    updtmsg["tags"] = {"ticker": symbol, "exchange": "poloniex"}
                    updtmsg["fields"] = dict()
                    updtmsg["fields"]['value'] = float(exFetT[symbol][ml])
                    updtlist.append(updtmsg)

        self.newtickers = updtlist