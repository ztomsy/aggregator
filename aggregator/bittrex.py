import ccxt
import sys
from .exconfig import Settings


class Bittrex:

    ex = ...  # type: ccxt.base

    def __init__(self):
        self.curtickers = []

    def loadexchange(self):
        try:
            self.ex = ccxt.bittrex(
                {"apiKey": Settings.bittrex1ApiKey, "secret": Settings.bittrex1Sec})
        except Exception as e:
            print('Initialising bittrex: ', type(
                e).__name__, "!!!", e.args, ' ')

    def fetchtickers(self):
        try:
            exFetT = self.ex.fetch_tickers()
        except Exception as e:
            print('While fetching tickers next error occur: ',
                  type(e).__name__, "!!!", e.args)
            print("Exiting")
            sys.exit()

        updtlist = []

        for symbol in exFetT:
            if exFetT[symbol]['bid'] is not None:
                updtmsg = {}
                updtmsg["measurement"] = "ticker_data"
                updtmsg["tags"] = {"ticker": symbol, "exchange": "bittrex"}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['bid'] = exFetT[symbol]['bid']
                updtmsg["fields"]['ask'] = exFetT[symbol]['ask']
                updtmsg["fields"]['last'] = exFetT[symbol]['last']
                updtlist.append(updtmsg)

        self.curtickers = updtlist

    def splittickers(self):
        try:
            exFetT = self.ex.fetch_tickers()
        except Exception as e:
            print('While fetching tickers next error occur: ',
                  type(e).__name__, "!!!", e.args)
            print("Exiting")
            sys.exit()

        updtlist = []

        measurementlist = ['bid', 'ask', 'last']

        for symbol in exFetT:
            for ml in measurementlist:
                if exFetT[symbol][ml] is not None:
                    updtmsg = {}
                    updtmsg["measurement"] = ml
                    updtmsg["tags"] = {"ticker": symbol, "exchange": "bittrex"}
                    updtmsg["fields"] = dict()
                    updtmsg["fields"]['value'] = float(exFetT[symbol][ml])
                    updtlist.append(updtmsg)

        self.newtickers = updtlist

