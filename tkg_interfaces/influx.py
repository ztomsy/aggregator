from influxdb import InfluxDBClient


class Influx:

    def __init__(self):
        self.client = InfluxDBClient('18.182.117.179', 8086, 'write_data', 'write_data', 'TKG')
        # self.client = InfluxDBClient('13.231.173.161', 8086, 'write_data', 'write_data', 'TKG') # old db
        # self.client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'TKG') # local db
        # self.client = InfluxDBClient('13.231.128.28', 8086, 'write_data', 'write_data', 'TKG_ticker_data')
        # self.client = InfluxDBClient('18.179.13.172', 8086, 'admin', 'admin', 'TKG') # Nightly build

    def writepoints(self, rightjson):
        try:
            self.client.write_points(rightjson)
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('Writing data to InfluxDB failed: ', type(e).__name__, "-=-=-", e.args, '-=-=-', str(e))
    # --------------------------------------
    #




