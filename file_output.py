import logging

logging.basicConfig(filename='bitcoin_value.log', level=logging.DEBUG,
                                format='%(asctime)s - %(levelname)s - %(message)s')

results = [
{'pair': 'BTC_ETH', 'globalTradeID': '201710399', 'tradeID': '31628612', 'date': '2017-07-31 18:58:27', 'type': 'sell', 'rate': '0.07160037', 'amount': '0.00211577', 'total': '0.00015148'},
{'pair': 'GJS_ETH', 'globalTradeID': '201710396', 'tradeID': '31628610', 'date': '2017-07-31 18:58:26', 'type': 'sell', 'rate': '0.07160037', 'amount': '0.02000000', 'total': '0.00143200'},
{'pair': 'BTC_ETH', 'globalTradeID': '201710400', 'tradeID': '31628613', 'date': '2017-07-31 18:59:00', 'type': 'buy', 'rate': '0.07200000', 'amount': '0.00211577', 'total': '0.00015148'},
{'pair': 'GJS_ETH', 'globalTradeID': '2017103401', 'tradeID': '31628620', 'date': '2017-07-31 18:59:30', 'type': 'buy', 'rate': '0.071500000', 'amount': '0.02000000', 'total': '0.00143200'}
]

logging.debug(" ********************************* ")

open_files = {}
for i in range(0, len(results)):
    filename = results[i].get('pair')
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
    if (results[i].get('type') == 'sell'):
        handle.write(results[i].get('globalTradeID') + ','
                      + results[i].get('tradeID') + ','
                      + results[i].get('date') + ','
                      + results[i].get('rate') + '\n')
    else:
         handle.write(',,,,,,' +
                     results[i].get('globalTradeID') + ','
                     + results[i].get('tradeID') + ','
                     + results[i].get('date') + ','
                     + results[i].get('rate') + '\n')
# close all files opened
for key in open_files.keys():
    (open_files.get(key)).close()
    if (open_files.get(key)).closed :
        logging.debug(key + " is closed")
