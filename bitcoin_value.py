#
# Copyright (C) Greg Smith smithgj66@hotmail.com - All Rights Reserved
#
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Greg Smith smithgj66@hotmail.com, August 2017
#
# input file format:
#       log_level = debug
#       BTC_ETH
#       BTC_STEEM

import os
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



def get_quote(coins, seconds):
    # https://poloniex.com/public?command=returnTradeHistory&currencyPair=BTC_NXT&start=1410158341&end=1410499372
    url1 = 'https://poloniex.com/public?command=returnTradeHistory'
    curr_pair = '&currencyPair=' + coins
    curr_time = arrow.utcnow()
    start = '&start=' + str(curr_time.timestamp - seconds)
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

def writelist2files(results):
    open_files = {}
    for i in range(0, len(results)):
        logging.debug('results =')
        logging.debug(results)
        # check for empty list
        if results[i] == []:
            continue
        filename = results[i][0].get('pair')
        # CASE 1 file has already been opened for writing
        if (filename in open_files):
            handle = open_files[filename]
        else:
            # CASE 2 if file can be opened, we want to open it for writing,
            #        but not write the headers
            try:
                handle = open("%s.csv" % filename, "r")
                handle.close()
                handle = open("%s.csv" % filename, "a+")
                open_files[filename] = handle
            # CASE 3 file doesn't exist, create it and add headers
            except FileNotFoundError:
                handle = open("%s.csv" % filename, "a+")
                open_files[filename] = handle
                handle.write('SELL,,,,,,BUY\n')
                handle.write('globalTradeID,tradeID,date,rate,,,globalTradeID,tradeID,date,rate\n')

        # write data to file, based on type = buy or sell
        for j in range(0, len(results[i])):
            if (results[i][j].get('type') == 'sell'):
                handle.write(results[i][j].get('globalTradeID') + ','
                             + results[i][j].get('tradeID') + ','
                             + results[i][j].get('date') + ','
                             + results[i][j].get('rate') + '\n')
            else:
                handle.write(',,,,,,' +
                             results[i][j].get('globalTradeID') + ','
                             + results[i][j].get('tradeID') + ','
                             + results[i][j].get('date') + ','
                             + results[i][j].get('rate') + '\n')
    # close all files opened
    for key in open_files.keys():
        (open_files.get(key)).close()
        if (open_files.get(key)).closed:
            logging.debug(key + " is closed")
    return()

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
    # check for "results" sub-directory, create if it doesn't exist,
    # and cd there now that we have read the input file and will be
    # outputting the results to .csv files
    if not(os.path.isdir("results")):
        try:
            os.mkdir("results", 0o777)
            os.chdir("results")
        except OSError:
            logging.warning("Could not create 'results' directory")
    # calculate how far back in time to go for the get_quote function
    # seconds = ((# of entries in input list) / 5 ) + 1 ; if <2 use 2
    seconds = (len(data_list)//5) + 1
    if (seconds < 2):
        seconds = 2

    while (True):
        data = []
        count = 0
        for i in range(0, len(data_list)):
            data_line = get_quote(data_list[i], seconds)
            trans_data = str2listofdicts(data_line, data_list[i])
            data.append(trans_data)
            count = count + 1
            if ((count % 5) == 0):
                time.sleep(1)
        writelist2files(data)
        time.sleep(1)

if __name__ == "__main__":
    go()