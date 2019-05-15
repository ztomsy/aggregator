import argparse

def Clipars(args):

    parser = argparse.ArgumentParser()

    parser.add_argument('-ft', '--fetchtype', type=str, required=True, help='''
    Fetch type.
    ticker = write tickers
    ob = orderbook data(look orderbook class docstring) 
    derivative = write derivative data
    tickmas = to wite different moving averages
    ohlcvind = to write indicators on ohlcv candle data
    ''')

    #can be parsed from exchange list defined above
    parser.add_argument('-ex', '--exchange', type=str, required=True, help='''
    Define exchange Name in accordance to ccxt notation''')

    parser.add_argument('-p', '--pause', type=float, required=False, default=0.5, help='''
    Define pause between fetching in seconds. Default is 0.5''')
    
    return parser.parse_args(args)
