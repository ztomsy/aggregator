import ccxt
import sys
from .exconfig import Settings

class Kucoin:

    ex = ...  # type: ccxt.base
    logger = None

    def __init__(self, logger: object = None):
        self.logger = logger
        self.curtickers = []


    @classmethod
    def loadexchange(self):
        """Load exchange"""
        try:
            self.ex = ccxt.kucoin({"apiKey": Settings.kucoin1['apiKey'], "secret": Settings.kucoin1['secret']})
        except Exception as e:
            self.logger.error('Initialising kucoin: ', type(e).__name__, "!!!", e.args, ' ')
            sys.exit()


    @classmethod
    def fetchtickers(self):
        """Fetch exchanges tickers and wrap it into updtlist"""
        try:
            exFetT = self.ex.fetch_tickers()
        except Exception as e:
            self.logger.error('While fetching tickers next error occur: ', type(e).__name__, "!!!", e.args)
            self.logger.error("Exiting")
            sys.exit()

        updtlist = []

        for symbol in exFetT:
            if exFetT[symbol]['bid'] is not None:
                updtmsg = {}
                updtmsg["measurement"] = "ticker_data"
                updtmsg["tags"] = {"ticker": symbol, "exchange": "kucoin"}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['bid'] = exFetT[symbol]['bid']
                updtmsg["fields"]['ask'] = exFetT[symbol]['ask']
                updtmsg["fields"]['last'] = exFetT[symbol]['last']
                updtmsg["fields"]['baseVolume'] = exFetT[symbol]['baseVolume']
                updtmsg["fields"]['quoteVolume'] = exFetT[symbol]['quoteVolume']
                updtmsg["fields"]['spread'] = float(exFetT[symbol]['ask']) - float(exFetT[symbol]['bid'])
                abmin = float(exFetT[symbol]['ask']) - float(exFetT[symbol]['bid'])
                abplus = float(exFetT[symbol]['ask']) + float(exFetT[symbol]['bid'])
                updtmsg["fields"]['spreadp'] = 2 * abmin / abplus
                updtlist.append(updtmsg)

        self.curtickers = updtlist
