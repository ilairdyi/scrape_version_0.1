from time import sleep
import json
from coin_glass.coin_glas_db import CoinGlass_DB
# used this to get all data https://fapi.coinglass.com/api/grayscaleOpenInterest/history?symbol= <- add BTC or ETH

class Get_Grayscaleholdings_Coin_Glass(CoinGlass_DB):

    def get_grayscale_info(self, url):
        """"""
        self.base_url = "https://fapi.coinglass.com/api/grayscaleOpenInterest/history?symbol="
        self.r = self.sessions.get(self.base_url + url, headers=self.coinglass_header, data=self.params)
        print(self.r, 'Grayscale Holdings -->', url)
        api_data = self.r.html.html
        raw_data = json.loads(api_data)
        # print(raw_data)
        return raw_data

    def filter_grayscale_holdings(self, data, url):

        holdings = data['data']['opList']
        price = data['data']['priceList']
        date = data['data']['dateList']

        db_list = []
        for (a, b ,c ) in zip(holdings, price, date):
            a = (url, str(a), str(b) ,str(c / 1000))
            a = list(a)
            db_list.append(a)

        # for x in db_list:
        #     print(x)

        print(db_list[-1])
        return db_list[-1]

    def upload_grayscale_holding(self, db_list):
        checker = self.insert_grayscale_holdings(id_list=db_list)
        if checker == False:
            print('FAILED ---> Grayscale holdings database did not save!')


    def call_all_grayscale_holding(self):
        crypto_list = ['BTC', 'ETH', 'LINK']
        for items in crypto_list:
            data = self.get_grayscale_info(items)
            db_list = self.filter_grayscale_holdings(data, items)
            self.upload_grayscale_holding(db_list)
            sleep(4)

# crypto_list = ['BTC', 'ETH', 'LINK']
#
#
# test = Get_Grayscaleholdings_Coin_Glass()
# db_test = CoinGlass_DB()
#
# for items in crypto_list:
#     data = test.get_grayscale_info(items)
#     test.filter_grayscale_holdings(data, items)
#     sleep(4)
