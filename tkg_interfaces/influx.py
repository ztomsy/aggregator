from influxdb import InfluxDBClient


class Influx:

    def __init__(self):
        self.client = InfluxDBClient('18.182.117.179', 8086, 'write_data', 'write_data', 'TKG')
        # self.client = InfluxDBClient('localhost', 8086, 'admin', 'admin', 'TKG') # local db

    def writepoints(self, rightjson):
        try:
            self.client.write_points(rightjson)
        except Exception as e:
            # print(type(e).__name__, e.args, str(e))
            print('Writing data to InfluxDB failed: ', type(e).__name__, "-=-=-", e.args, '-=-=-', str(e))

    def query(self, query):
        try:
            return self.client.query(query)
        except Exception as e:
            print('Querying data from InfluxDB failed: ', type(e).__name__, "-=-=-", e.args, '-=-=-', str(e))


