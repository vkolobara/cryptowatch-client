import logging
import os
import requests
import writer

class CryptoWatchClient(object):
    def __init__(self, exchange, out_file):
        self.exchange = exchange
        self.base_url = 'https://api.cryptowat.ch/markets/%s' % exchange
        self.out_file = out_file

    def get_ohlc(self, pair, periods = [60,180,300,21600,86400]):
        logging.info("Download OHLC for %s for periods %s" % (pair, str(periods)))
        latest_times = CryptoWatchClient.get_latest_times(self.exchange, pair, periods, self.out_file)
        after = min(latest_times)
        url = self.base_url + '/' + pair + '/ohlc?'
        params = '&'.join(["after=%s" % after, 
                           "periods=%s" % ','.join([str(p) for p in periods])])
        r = requests.get(url + params)
        ix = 0
        if r.status_code != 200:
            logging.error("The pair %s doesn't exist on exchange %s" % (pair, self.exchange))
        else:
            data = r.json()
            for period in data['result']:
                w = writer.CSVWriter(self.out_file + "_%s_%s_%s.csv" % (self.exchange, pair, period))
                rows = [x for x in data['result'][period] if int(x[0]) > latest_times[ix]]
                w.write(rows)
        logging.info("OHLC downloaded")

    @staticmethod
    def get_latest_times(exchange, pair, periods, file):
        ret = []
        for period in periods:
            file_name = file + "_%s_%s_%s.csv.last_time" % (exchange, pair, period)
            if os.path.exists(file_name):
                with open(file_name, 'r') as fil:
                    line = fil.readline()
                    if line != '':
                        ret.append(int(line))
                    else:
                        ret.append(0)
            else:
                ret.append(0)
        return ret
