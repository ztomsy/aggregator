import ccxt
import os
import sys
import time
import datetime

from influxdb import InfluxDBClient

# -------------------
#
# Binance Balance connector made throw ccxt to InfluxDB
# Old version with filtering while fetching
#
# -------------------


# Trying to load config file

if not os.path.exists("./exconfig.py"):
    print("Config not found")
    print("Create exconfig.py first")
    sys.exit(1)
else:
    import exconfig
    print("Config found")


# todo wrap parsing config file into function

# Wrapping config file to dicts

exNames = dict()
exNames[1] = exconfig.binance1Name
exNames[2] = exconfig.binance2Name
exNames[3] = exconfig.binance3Name
exNames[4] = exconfig.binance4Name
exNames[5] = exconfig.binance5Name
exNames[6] = exconfig.binance6Name


exCurs = dict()
exCurs[1] = exconfig.binance1Cur
exCurs[2] = exconfig.binance2Cur
exCurs[3] = exconfig.binance3Cur
exCurs[4] = exconfig.binance4Cur
exCurs[5] = exconfig.binance5Cur
exCurs[6] = exconfig.binance6Cur

exApiKeys = dict()
exApiKeys[1] = exconfig.binance1ApiKey
exApiKeys[2] = exconfig.binance2ApiKey
exApiKeys[3] = exconfig.binance3ApiKey
exApiKeys[4] = exconfig.binance4ApiKey
exApiKeys[5] = exconfig.binance5ApiKey
exApiKeys[6] = exconfig.binance6ApiKey

exApiSecrets = dict()
exApiSecrets[1] = exconfig.binance1Secret
exApiSecrets[2] = exconfig.binance2Secret
exApiSecrets[3] = exconfig.binance3Secret
exApiSecrets[4] = exconfig.binance4Secret
exApiSecrets[5] = exconfig.binance5Secret
exApiSecrets[6] = exconfig.binance6Secret

# define start time
ts_start = datetime.datetime.now()
print("Launch time: ", ts_start)

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
        return save_balances_to_dict(excBalance, excTickers, exName) #### todo Have to return dicts and call for function in main ###

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


def rightname(cur_cur):
    if cur_cur.upper() != 'USDT':
        return "%s/BTC" % cur_cur.upper()
    else:
        return "BTC/USDT"

# todo Create pure balance fetch function

def save_balances_to_dict(exBalance, exTicker, exName):
    # output the result for each non zero currency which BTC amount more then 0.00005
    # define new return dict
    updtmsg = {}
    #updtMsg['exData'] = []
    # Total_BTC_amount
    totalitarian = 0
    # fill updtMsg dict
    # write data in next format: [{"measurement":"Balances","tags":{"tkgid":"bta3"},"fields":{"BTC":0.64456585,"ETH":3.01}}]
    updtmsg["measurement"] = "balances"
    updtmsg["tags"] = {"tkgid":exName}
    updtmsg["fields"] = dict()

    for cur_cur in exBalance['total'].keys():
        if exBalance['total'][cur_cur] > 0.0001:
            if cur_cur == 'BTC':
                updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                totalitarian = totalitarian + exBalance['total'][cur_cur]
            elif cur_cur == 'USDT':
                updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                totalitarian = totalitarian + exBalance['total'][cur_cur] / exTicker[rightname(cur_cur)]['close']
            elif rightname(cur_cur) in exTicker:
                cur_cur_btcprice = exTicker[rightname(cur_cur)]['close']
                if exBalance['total'][cur_cur] * cur_cur_btcprice > 0.00005:
                    updtmsg["fields"][cur_cur] = exBalance['total'][cur_cur]
                    totalitarian = totalitarian + exBalance['total'][cur_cur] * cur_cur_btcprice

    updtmsg["fields"]['TotalBTC'] = totalitarian
    updtmsg["fields"]['TotalETH'] = totalitarian / exTicker[rightname('ETH')]['close']
    updtmsg["fields"]['TotalUSDT'] = float(totalitarian * exTicker[rightname('USDT')]['close'])

    updtlist = []
    updtlist = [updtmsg]

    return updtlist

def main():
    try:

        # Connect to DB
        # client = InfluxDBClient('localhost', 8086, 'root', 'root', 'TKG')
        client = InfluxDBClient('18.182.117.179', 8086, 'write_data', 'write_data', 'TKG')
        curTick = 1

        while True:
            # save data as json to influx DB to table Balances with service ID
            # define ex amounts
            for i in range(1,len(exNames)+1):
                time.sleep(5.0)
                # connect to exchange and get necessery dict
                myDict = myBalance(exApiKeys[i], exApiSecrets[i], exNames[i])
                # check for proper responce
                if len(myDict[0]['fields']) > 0:
                    #todo need exceptions for writing to db
                    client.write_points(myDict)
                    msg1 = "# %s %s %s storages updated " % (curTick, datetime.datetime.now(), exNames[i])
                    print(msg1)
                    curTick = curTick + 1

    except KeyboardInterrupt:
        print('Interrupted by keyboard.')


if __name__ == '__main__':
    main()