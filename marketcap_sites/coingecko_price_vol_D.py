from time import sleep
import json
from marketcap_sites.marketcaps_db import Marketcaps_DB

class Get_Price_Vol_Coin_Gecko(Marketcaps_DB):

    def get_price_vol(self, url , ticker):
        self.r = self.sessions.get(url, headers=self.header)
        print(self.r, ticker, 'Price and Vol' )
        api_data = self.r.html.html
        raw_data = json.loads(api_data)
        # print(raw_data)

        return raw_data

    def filter_exchange_flow(self, data, url, ticker):

        price = data['stats']
        vol = data['total_volumes']

        db_list = []
        for (a, b) in zip(price, vol):
            a = (ticker, a[0] /1000, "{:.2f}".format(a[1]), int(b[1]))
            a = list(a)
            db_list.append(a)

        for x in db_list[-1:]:
            print(x)

        return db_list

    def upload_db(self, db_list):
        checker = self.insert_price_vol_coingeckco(id_list=db_list[-1])
        if checker == False:
            print('FAILED ---> Marketcaps - Price and Vol database did not save!')

    def call_all(self):
        # List of websites to scrape from
        url_list = [['https://www.coingecko.com/price_charts/1/usd/max.json', 'BTC'],
                    ['https://www.coingecko.com/price_charts/279/usd/max.json', 'ETH'],
                    ['https://www.coingecko.com/price_charts/325/usd/max.json', 'USDT'],
                    ['https://www.coingecko.com/price_charts/6319/usd/max.json', 'USDC'],
                    ['https://www.coingecko.com/price_charts/877/usd/max.json', 'LINK']
                    ]

        for url in url_list:
            data = self.get_price_vol(url[0], url[1])
            db_list = self.filter_exchange_flow(data, url[0], url[1])
            self.upload_db(db_list)
            sleep(4)


# test = Get_Price_Vol_Coin_Gecko()
# db_test = Marketcaps_DB()
# for url in url_list:
#     data = test.get_price_vol(url[0], url[1])
#     test.filter_exchange_flow(data,url[0], url[1])
#     sleep(4)
#
