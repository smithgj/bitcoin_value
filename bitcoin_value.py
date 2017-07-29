# Greg Smith smithgj66@hotmail.com
#
#
# input file format:
#       log_level = debug
#       BTC_ETH
#       BTC_STEEM


import logging


logging.basicConfig(filename='bitcoin_value.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)


def read_file():
    input_data = []
    return(input_data)


def go():
    pass

if __name__ == "__main__":
    go()