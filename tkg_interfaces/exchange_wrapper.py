import ccxt


class ExchangeWrapperError(Exception):
    """Basic exception for errors raised by ccxtExchangeWrapper"""
    pass

class ExchangeWrapperOfflineFetchError(ExchangeWrapperError):
    """Exception for Offline fetching errors"""
    pass

class ccxtExchangeWrapper:

    _ccxt = ...  # type: ccxt.Exchange

    @classmethod
    def load_from_id(cls, exchange_id, api_key="", secret=""):

        try:
            exchange = getattr(exchanges, exchange_id)
            exchange = exchange(exchange_id, api_key, secret)
            return exchange
        except AttributeError:
            return cls(exchange_id, api_key, secret, offline)

    def __init__(self, exchange_id, api_key="", secret=""):

        exchange = getattr(ccxt, exchange_id)

        self._ccxt = exchange({'apiKey': api_key, 'secret': secret})
        self.wrapper_id = "generic"

        self.tickers = dict()
        self.markets = dict()

    # generic method for loading markets could be redefined in custom exchange wrapper
    def _load_markets(self):
        return self._ccxt.load_markets()

    # generic method for fetching tickers could be redefined in custom exchange wrapper
    def _fetch_tickers(self):
        return self._ccxt.fetch_tickers()

    # generic method for fetching ohlcv
    def _fetch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None):
        return self._ccxt.fetch_ohlcv(symbol, symbol, timeframe, since, limit, params={})

    # generic method for fetching orderbook
    def _fetch_order_book(self, symbol):
        return self._ccxt.fetch_order_book(self, symbol, limit=None, params={})


    def get_exchange_wrapper_id(self):
        return "generic"

