#!/bin/python

import os
import requests
import time
import datetime

from influxdb import InfluxDBClient


if not os.path.exists("./exconfig.py"):
    print("Config not found")
    print("Create exconfig.py first")
    sys.exit(1)
else:
    import exconfig
    print("Config found")

# Wrapping config file to list
ethWlts = (exconfig.eth1key, exconfig.eth2key)


def build_multi_balance_url(addresses):
    # Build url for multiwallets fetch like: https://api.etherscan.io/api?module=account&action=balancemulti&address=0x38479e732293B8666e631C32deA160f8291234eC,0x2C52b7c94132065AA204Eb8f087AC2E8881C51C9
    adrstring = ",".join(map(str, addresses))
    url = 'https://api.etherscan.io/api?module=account&action=balancemulti&address=%s' % (adrstring)
    return url


def build_single_balance_url(address):
    # Build url for single fetch like: https://api.etherscan.io/api?module=account&action=balance&address=0x38479e732293B8666e631C32deA160f8291234eC
    url = 'https://api.etherscan.io/api?module=account&action=balance&address=%s' % (address)
    return url


def raw_get_balances(url):
    raw = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    return raw

def get_balances(url, address):

    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})

    mydict = html.json()

    # return html.json()
    # wrap smsn like {"status":"1","message":"OK","result":"30010000000000000000"}

    if mydict['message'] == 'OK':
        updtmsg = {}
        # fill updtMsg dict
        # write data in next format: [{"measurement":"Balances","tags":{"tkgid":"bta3"},"fields":{"BTC":0.64456585,"ETH":3.01}}]
        updtmsg["measurement"] = "Balances"
        updtmsg["tags"] = {"address": address}
        updtmsg["fields"] = dict()
        updtmsg["fields"]['balance'] = mydict['result']
        updtlist = []
        updtlist = [updtmsg]

    return updtlist

def main():
    try:

        # Connect to DB
        client = InfluxDBClient('localhost', 8086, 'root', 'root', 'TKG')

        curTick = 1

        while True:
            for i in range(0,len(ethWlts)):
                time.sleep(1000.0)
                # connect to wallet and get right dict
                myDict = get_balances(build_single_balance_url(ethWlts[i]), ethWlts[i])
                # check for proper responce
                if len(myDict[0]['fields']) > 0:
                    #print("Write points: {0}".format(myDict))
                    #todo need exceptions for writing to db
                    client.write_points(myDict)
                    msg1 = "# %s %s storages updated " % (curTick, datetime.datetime.now())
                    print(msg1)
                    curTick = curTick + 1

    except KeyboardInterrupt:
        print('Interrupted by keyboard.')


if __name__ == '__main__':
    main()