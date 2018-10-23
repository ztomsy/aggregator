import ccxt
import sys
# use networkX to find all triangles on graph
import networkx as nx
import numpy as np

from .exconfig import settings

class Binance():

    ex = ... # type: ccxt.base

    def __init__(self):
        self.curtickers = []
        self.newtickers = []
        self.curderivatives = []
        # self.updtlist = []

    def loadexchange(self):
        # Load exchange
        try:
            self.ex = ccxt.binance({"apiKey": settings.binance1ApiKey, "secret": settings.binance1Secret})
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('While initialising Kucoin: ', type(e).__name__, "!!!", e.args, ' ')
            # print("Exiting")
            # sys.exit()

    def fetchtickers(self):
        # Fetch exchanges ticker for necessary pair
        try:
            exFetT = self.ex.fetch_bids_asks()
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
            if exFetT[symbol]['bid'] is not None and exFetT[symbol]['ask'] is not None and exFetT[symbol]['bid'] != 0 and exFetT[symbol]['ask'] != 0:
                updtmsg = {}
                updtmsg["measurement"] = "ticker_data"
                updtmsg["tags"] = {"ticker": symbol, "exchange": "binance"}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['bid'] = exFetT[symbol]['bid']
                updtmsg["fields"]['ask'] = exFetT[symbol]['ask']
                updtmsg["fields"]['last'] = exFetT[symbol]['last']
                updtmsg["fields"]['spread'] = float(exFetT[symbol]['ask']) - float(exFetT[symbol]['bid'])
                abmin = float(exFetT[symbol]['ask']) - float(exFetT[symbol]['bid'])
                abplus = float(exFetT[symbol]['ask']) + float(exFetT[symbol]['bid'])
                updtmsg["fields"]['spreadp'] = 2 * abmin / abplus 
                updtlist.append(updtmsg)

        self.curtickers = updtlist

#        move to another class-file construction
#       ------------------------------------------

    @staticmethod
    def get_basic_triangles_from_markets(markets):
        graph = nx.Graph()
        for symbol in markets:

            if markets[symbol]["active"]:
                graph.add_edge(markets[symbol]['base'], markets[symbol]['quote'])

        # finding the triangles as the basis cycles in graph
        triangles = list(nx.cycle_basis(graph))


        #todo find 4+ cliques, define order, build new list with directions and count em
        # cliques = list(nx.find_cliques(graph))
        # newcliquelist = []
        # for a in cliques:
        #     if len(a)>3:
        #         newcliquelist.append(a)
        # print(newcliquelist)



        return triangles

    @staticmethod
    def get_all_triangles(triangles: list, start_currencies: list):

        filtered_triangles = list()

        for start_currency in start_currencies:
            for cur in triangles:
                if start_currency in cur:
                    p = cur.index(start_currency)
                    if p > 0:
                        cur = np.roll(cur, 3 - p).tolist()

                    filtered_triangles.append(list((start_currency, cur[1], cur[2])))
                    filtered_triangles.append(list((start_currency, cur[2], cur[1])))

        return filtered_triangles

    @staticmethod
    def fill_triangles(triangles: list, start_currencies: list, tickers: dict, commission=0):
        tri_list = list()

        for t in triangles:
            tri_name = "-".join(t)

            if start_currencies is not None and t[0] in start_currencies:
                tri_dict = dict()
                result = 1.0

                for i, s_c in enumerate(t):

                    source_cur = t[i]
                    dest_cur = t[i + 1] if i < len(t) - 1 else t[0]

                    symbol = ""
                    order_type = ""
                    price_type = ""

                    if source_cur + "/" + dest_cur in tickers:
                        symbol = source_cur + "/" + dest_cur
                        order_type = "sell"
                        price_type = "bid"

                    elif dest_cur + "/" + source_cur in tickers:
                        symbol = dest_cur + "/" + source_cur
                        order_type = "buy"
                        price_type = "ask"

                    if symbol in tickers and price_type in tickers[symbol] and tickers[symbol][price_type] is not None \
                            and tickers[symbol][price_type] > 0:

                        price = tickers[symbol][price_type]

                        if result != 0:
                            result = result / price if order_type == "buy" else result * price
                            result = result * (1 - commission)

                    else:
                        price = 0
                        result = 0

                    leg = i + 1

                    tri_dict["triangle"] = tri_name
                    tri_dict["cur" + str(leg)] = t[i]
                    tri_dict["symbol" + str(leg)] = symbol
                    tri_dict["leg{}-order".format(str(leg))] = order_type
                    tri_dict["leg{}-price".format(str(leg))] = price

                if result != 0:
                    tri_dict["leg-orders"] = tri_dict["leg1-order"] + "-" + tri_dict["leg2-order"] + "-" + \
                                             tri_dict["leg3-order"]

                tri_dict["result"] = result

                tri_list.append(tri_dict)

        return tri_list

#
#----------------------------------
# 

    def fetchderivatives(self):
        # Fetch exchanges ticker for necessary pair
        try:
            exFetT = self.ex.fetch_bids_asks()
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('While fetching tickers next error occur: ', type(e).__name__, "!!!", e.args)
            print("Exiting")
            sys.exit()
        # Wrap raw ticker data from ccxt into list of necessary triangles result dicts

        # define new return dict and list
        updtlist = []

        # define triangle lists
        trilist = []
        filteredtrilist = []
        finaltrilist = []

        # define start currencies list
        # todo get quote currencies list from exchange by adding uniqe quote currencies into list
        startcurlist = ['USDT', 'BTC', 'ETH']

        trilist = self.get_basic_triangles_from_markets(self.ex.markets)
        filteredtrilist = self.get_all_triangles(trilist, startcurlist)
        finaltrilist = self.fill_triangles(filteredtrilist, startcurlist, exFetT, 0.005)

        for tri in finaltrilist:
            if tri["result"] is not None:
                updtmsg = {}
                updtmsg["measurement"] = "ticker_derivatives"
                updtmsg["tags"] = {"ticker": tri["triangle"], "exchange": "binance"}
                updtmsg["fields"] = dict()
                updtmsg["fields"]['result'] = tri['result']
                updtlist.append(updtmsg)

        self.curderivatives = updtlist


    def splittickers(self):
        # Fetch exchanges ticker for necessary pair
        try:
            exFetT = self.ex.fetch_bids_asks()
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
        updtlist2 = []
        # define measurement list
        measurementlist = ['bid', 'ask', 'last']

        for symbol in exFetT:
            for ml in measurementlist:
                if exFetT[symbol][ml] is not None:
                    updtmsg = {}
                    updtmsg["measurement"] = ml
                    updtmsg["tags"] = {"ticker": symbol, "exchange": "binance"}
                    updtmsg["fields"] = dict()
                    updtmsg["fields"]['value'] = float(exFetT[symbol][ml])
                    updtlist2.append(updtmsg)

        self.newtickers = updtlist2

    def myBalance(exApikey, exSec, exName):
        try:
            # Fetch account balance from an exchange
            # only binance now!
            print('Connecting to %s...' % exName)
            exc = ccxt.binance({'apiKey': exApikey, 'secret': exSec})
            excBalance = exc.fetch_balance()
            time.sleep(5.0)
            # Fetch tickers from an exchange
            print('Fetching tickers from %s...' % exName)
            excTickers = exc.fetch_tickers()
            return _save_balances_to_dict(excBalance, excTickers,
                                         exName)  #### todo Have to return dicts and call for function in main ###

        except ccxt.DDoSProtection as e:
            print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
            return {}
        except ccxt.RequestTimeout as e:
            print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
            return {}
        except ccxt.ExchangeNotAvailable as e:
            print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')
            return {}
        except ccxt.AuthenticationError as e:
            print(type(e).__name__, e.args, 'Authentication Error (missing API keys, ignoring)')
            return {}

    @staticmethod
    def _rightname(cur_cur): # todo Check TrueUSD currtnce status to ETH and BTC
        if cur_cur.upper() != 'USDT':
            return "%s/BTC" % cur_cur.upper()
        else:
            return "BTC/USDT"

    # todo Create pure balance fetch function
    @staticmethod
    def _save_balances_to_dict(exBalance, exTicker, exName):
        # output the result for each non zero currency which BTC amount more then 0.00005
        # define new return dict
        updtmsg = {}
        # updtMsg['exData'] = []
        # Total_BTC_amount
        totalitarian = 0
        # fill updtMsg dict
        # write data in next format: [{"measurement":"Balances","tags":{"tkgid":"bta3"},"fields":{"BTC":0.64456585,"ETH":3.01}}]
        updtmsg["measurement"] = "Balances"
        updtmsg["tags"] = {"tkgid": exName}
        updtmsg["fields"] = dict()

        for cur_cur in exBalance['total'].keys():
            if exBalance['total'][cur_cur] > 0.0001:
                if cur_cur == 'BTC':
                    updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                    totalitarian = totalitarian + exBalance['total'][cur_cur]
                elif cur_cur == 'USDT':
                    updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                    totalitarian = totalitarian + exBalance['total'][cur_cur] / exTicker[_rightname(cur_cur)]['close']
                elif rightname(cur_cur) in exTicker:
                    cur_cur_btcprice = exTicker[rightname(cur_cur)]['close']
                    if exBalance['total'][cur_cur] * cur_cur_btcprice > 0.00005:
                        updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                        totalitarian = totalitarian + exBalance['total'][cur_cur] * cur_cur_btcprice

        updtmsg["fields"]['TotalBTC'] = totalitarian
        updtmsg["fields"]['TotalETH'] = totalitarian / exTicker[_rightname('ETH')]['close']
        updtmsg["fields"]['TotalUSDT'] = float(totalitarian * exTicker[_rightname('USDT')]['close'])

        updtlist = []
        updtlist = [updtmsg]

        return updtlist