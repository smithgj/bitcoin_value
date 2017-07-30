# Greg Smith smithgj66@hotmail.com
#
#
# input file format:
#       log_level = debug
#       BTC_ETH
#       BTC_STEEM


import logging
import time
import arrow
import requests


def get_quote(coins):
    # https://poloniex.com/public?command=returnTradeHistory&currencyPair=BTC_NXT&start=1410158341&end=1410499372
    url1 = 'https://poloniex.com/public?command=returnTradeHistory'
    curr_pair = '&currencyPair=' + coins
    curr_time = arrow.utcnow()
    start = '&start=' + str(curr_time.timestamp - 15)
    end = '&end=' + str(curr_time.timestamp)
    quote_url = url1 + curr_pair + start + end
    logging.debug(quote_url)
    r = requests.get(quote_url)
    logging.debug(r)
    return('dummy data')

def read_file():
    input_data = []
    with open('bv_inputs.txt') as f:
        input_data = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
        input_data = [x.strip() for x in input_data]
    return(input_data)

def go():
    data_list = read_file()
    # get log level, and remove it from data_list
    if (data_list[0].startswith("log_level")):
        log_level = data_list.pop(0)
        log_level = log_level[(log_level.find('=') + 1):]
        log_level = log_level.strip()
        if (log_level.upper() in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            logging.basicConfig(filename='bitcoin_value.log', level=logging.log_level.upper(),
                                format='%(asctime)s - %(levelname)s - %(message)s')
            # logging.disable(logging.DEBUG)
        else:
            file = open('bitcoin_value.log', 'w')
            file.write('logging level could not be set.')
    while (true):
        count = 0
        for i in range(0, len(data_list)):
            get_quote(i)
            count = count + 1
            if ((count % 5) == 0):
                sleep(1)
        #TODO write data to csv files
        sleep(1)

if __name__ == "__main__":
    go()