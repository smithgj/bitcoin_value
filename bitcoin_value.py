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

def wait(msec):
    pass


def go():
    data_list = read_file()
    while (true):
        count = 0
        for i in range(0, len(data_list)):
            #TODO get quote
            count = count + 1
            if ((count % 5) == 0):
                wait(1000)
        #TODO write data to csv files
        wait(1000)

if __name__ == "__main__":
    go()