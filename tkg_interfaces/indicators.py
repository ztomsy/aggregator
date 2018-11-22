import numpy as np

def computeRSI(prices, n=14):
    '''
    Return RSI for n last entries
    :param prices: list of float
    :param n: int
    :return: ndarray [44.56611005 44.56611005 44.56611005...
    '''
    deltas = np.diff(prices)
    seed = deltas[:n + 1]
    up = seed[seed >= 0].sum() / n
    down = -seed[seed < 0].sum() / n
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100. / (1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi

def computeMA(prices, window):
    '''
    Return ma from window
    :param prices: list of float
    :param window: int
    :return: ndarray [4630.719 4631.027 4630.9...
    '''
    weigths = np.repeat(1.0, window) / window
    smas = np.convolve(prices, weigths, 'valid')
    return smas  # as a numpy array

def computeEMA(prices, window):
    '''
    Return ema from window
    :param prices: list of float
    :param window: int
    :return: ndarray [4630.719 4631.027 4630.9...
    '''
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(prices, weights, mode='full')[:len(prices)]
    a[:window] = a[window]
    return a

def computeMACD(x, slow=26, fast=12):
    '''
    compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
    return value is emaslow, emafast, macd which are len(x) arrays
    :param x: list of float
    :param slow: int
    :param fast: int
    :return: 3 x ndarray
    '''
    emaslow = computeEMA(x, slow)
    emafast = computeEMA(x, fast)
    return emafast - emaslow, emaslow, emafast
