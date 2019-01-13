import sys
import tkg_interfaces as TKG
from datetime import datetime

####################
# option = TKG.Clipars(sys.argv[1:])
####################


def main():
    try:
        symbol = "BTC/USDT"
        # define counter
        curtick = 0
        # initialize exchange
        exc = TKG.Binance()
        # load exchange
        exc.loadexchange()
        # create orderbook
        ob1 = TKG.Orderbook1()

        while True:
            # load ob
            try:
                exFetobs = exc.ex.fetch_order_book(symbol)  # fetch_order_book(symbol, limit=100)
            except Exception as e:
                # print(type(e).__name__, e.args, str(e))
                print('While fetching orderbook next error occur: ', type(e).__name__, "!!!", e.args)
                print("Exiting")
                sys.exit()
            ob1.update_ob(exFetobs)
            print(ob1.report_top_of_book())
            # Wrap ob from ccxt into our ob class
            # ob1._bid_book = exFetobs['bids']
            # ob1._ask_book = exFetobs['asks']
            # Or we can crete indexed by prices dict
            # for _ in exFetobs['bids']:
            #     ob1._bid_book[_[0]] = _[1]
            # for _ in exFetobs['asks']:
            #     ob1._ask_book[_[0]] = _[1]

            # # So we relay on ccxt in terms of sorting in that way
            # best_bid_price = ob1._bid_book[0][0]
            # best_bid_size = ob1._bid_book[0][1]
            # best_ask_price = ob1._ask_book[0][0]
            # best_ask_size = ob1._ask_book[0][1]
            # timenow = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] # slicing nanoseconds precision
            # tob = {'timestamp': timenow,
            #        'best_bid': best_bid_price,
            #        'bid_size': best_bid_size,
            #        'best_ask': best_ask_price,
            #        'ask_size': best_ask_size,
            #        'mid_price': int((best_ask_price+best_bid_price)/2)
            #        }

            #ob1._top_book_states.append(ob1.report_tob_data(time.time_ns()))


            curtick = curtick + 1
            time.sleep(0.5)

    except KeyboardInterrupt:
        print('Interrupted by keyboard.')

if __name__ == '__main__':
    main()