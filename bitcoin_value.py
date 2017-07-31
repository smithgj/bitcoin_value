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

def str2listofdicts(txt, pair):
    logging.debug('str2listofdicts')
    # strip of square brackets
    txt = txt[1:]
    txt = txt[:-1]
    trans_list_strs = []
    trans_list_dicts = []
    logging.debug(txt)
    items = txt.count('{')
    logging.debug("items = " + str(items))
    for i in range (0, items):
        str1 = txt[txt.find('{'):txt.find('}') + 1]
        trans_list_strs.append(str1)
        txt = txt[txt.find('}') + 2 :]
    # at this point trans_list_strs is a list of strings,
    #  next the strings need to be converted to dicts
    logging.debug(trans_list_strs)
    for j in range (0, len(trans_list_strs)):
        str1 = trans_list_strs[j][1:]
        str1 = str1[:-1]
        kv = str1.split(',')
        keys = []
        values = []
        keys.append("pair")
        values.append(pair)
        for k in range (0, len(kv)):
            key = kv[k][:kv[k].find(':')]
            key = key.replace('"','')
            value = kv[k][kv[k].find(':') + 1 : ]
            value = value.replace('"', '')
            keys.append(key)
            values.append(value)
        trans_list_dicts.append(dict(zip(keys, values)))
        logging.debug(trans_list_dicts)
    logging.debug('leaving str2listofdicts')
    return trans_list_dicts



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
    logging.debug(r.text)
    return(r.text)

def read_file():
    with open('bv_inputs.txt') as f:
        input_data = f.readlines()
        # remove whitespace characters like `\n` at the end of each line
        input_data = [x.strip() for x in input_data]
    return(input_data)

def writelist2files(list):
    pass
    # x = "file1"
    # h = open("%s.html" % x, "w")
    # h.close

def go():
    data_list = read_file()
    # get log level, and remove it from data_list
    if (data_list[0].startswith("log_level")):
        log_level = data_list.pop(0)
        log_level = log_level[(log_level.find('=') + 1):]
        log_level = log_level.strip()
        log_level = log_level.upper()
        if (log_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']):
            my_level = logging.getLevelName(log_level)
            logging.basicConfig(filename='bitcoin_value.log', level=my_level,
                                format='%(asctime)s - %(levelname)s - %(message)s')
            # logging.disable(logging.DEBUG)
        else:
            file = open('bitcoin_value.log', 'w')
            file.write('logging level could not be set.')
    while (True):
        trans_data = []
        data = []
        count = 0
        for i in range(0, len(data_list)):
            data_line = get_quote(data_list[i])
            trans_data = str2listofdicts(data_line, data_list[i])
            data.append(trans_data)
            count = count + 1
            if ((count % 5) == 0):
                time.sleep(1)
        #TODO write data to csv files now that we went through the input file
        writelist2files(data)
        time.sleep(1)

if __name__ == "__main__":
    go()