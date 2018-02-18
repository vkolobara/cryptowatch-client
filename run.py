import logging_conf
import logging
from client import CryptoWatchClient
from config import config

def main():
    client = CryptoWatchClient('bitfinex', 'data/ohlc')
    for pair in config['pairs']:
        client.get_ohlc(pair)

if __name__ == '__main__':
    logging.info("Application started")
    main()
    logging.info("Application done")
