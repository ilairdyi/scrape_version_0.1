from time import sleep
import json
from coin_glass.coin_glas_db import CoinGlass_DB

# used this to get all data https://fapi.coinglass.com/api/grayscaleOpenInterest/history?symbol= <- add BTC or ETH

class Get_Exchange_Flow_Coin_Glass(CoinGlass_DB):

    def get_exchange_data(self):
        """"""
        self.base_url = 'https://fapi.coinglass.com/api/exchange/chain/v2/balance?exName=all'
        self.r = self.sessions.get(self.base_url, headers=self.coinglass_header, data=self.params)
        print(self.r, 'Getting Exchange Flow data')
        api_data = self.r.html.html
        raw_data = json.loads(api_data)
        # print(raw_data)

        return raw_data

    def filter_exchange_flow(self, data):

        huobi = data['data']['dataMap']['Huobi']
        coincheck = data['data']['dataMap']['Coincheck']
        kraken = data['data']['dataMap']['Kraken']
        binance = data['data']['dataMap']['Binance']
        coinbase_pro = data['data']['dataMap']['Coinbase Pro']
        gate = data['data']['dataMap']['Gate']
        okex = data['data']['dataMap']['Okex']
        poloniex = data['data']['dataMap']['Poloniex']
        bitflyer = data['data']['dataMap']['Bitflyer']
        try:
            while True:
                bitflyer[bitflyer.index(None)] = 0
        except ValueError:
            pass
        bitfinex = data['data']['dataMap']['Bitfinex']
        bitstamp = data['data']['dataMap']['Bitstamp']
        bittrex = data['data']['dataMap']['Bittrex']
        datelist = data['data']['dateList']

        db_list = []
        for (a, b, c, d, e, f, g, h, i, j, k, l, m) in zip(huobi, coincheck, kraken, binance, coinbase_pro,
                                                 gate, okex, poloniex, bitflyer, bitfinex, bitstamp,
                                                 bittrex, datelist):
            alltogether = (a, b, c, d, e, f, g, h, i, j, k, l, m)
            for items in alltogether:
                if items == None:
                    items = 0
                    sleep(7)
            # print(alltogether)
            total = (a + b + c + d + e + f + g + h + i + j + k + l)
            complete = (a, b, c, d, e, f, g, h, i, j, k, l, total, m / 1000)
            complete = list(complete)
            db_list.append(complete)

        # for x in db_list:
        #     print(x)
            # print(len(x))
        # print('')
        print(db_list[-1])

        return db_list[-1]

    def upload_exchange_flow(self, db_list):
        checker = self.insert_exchange_flows(id_list=db_list)
        if checker == False:
            print('FAILED ---> Exchange Flow CoinGlass database did not save!')

    def call_all_exchange_flow(self):
        data = self.get_exchange_data()
        db_list = self.filter_exchange_flow(data)
        self.upload_exchange_flow(db_list)





# test = Get_Exchange_Flow_Coin_Glass()
# db_test = CoinGlass_DB()
# data = test.get_exchange_data()
# test.filter_exchange_flow(data)