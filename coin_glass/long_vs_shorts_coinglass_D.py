import json
from time import sleep
from coin_glass.coin_glas_db import CoinGlass_DB

class Get_CoinGlass_Longs_VS_Shorts(CoinGlass_DB):

    def get_coinglass_long_vs_short(self, url):
        self.base_url = f'https://fapi.coinglass.com/api/futures/longShortChart?symbol={url}&timeType=5'
        self.r = self.sessions.get(self.base_url, headers=self.coinglass_header, data=self.params)
        print(self.r, 'Getting', url, 'Long vs Short data')
        api_data = self.r.text.encode('utf8')
        raw_data = json.loads(api_data)
        # print(raw_data)
        return raw_data

    def filter_long_vs_short(self, data, url):

        long_list = data['data']['longRateList']
        short_list = data['data']['shortsRateList']
        price_list = data['data']['priceList']
        ratio_list = data['data']['longShortRateList']
        date_list = data['data']['dateList']

        db_list = []
        for (a, b, c, d, e) in zip(long_list, short_list, price_list, ratio_list, date_list):
            a = (url, str(a), str(b), str(c), str(d), str(e / 1000))
            a = list(a)
            db_list.append(a)

        # for x in db_list:
        #     print(x)
        # print('')
        # print('')
        print(db_list[-1])

        return db_list[-1]

    def upload_long_vs_short(self, db_list):
        checker = self.insert_longs_vs_shorts(id_list=db_list)
        if checker == False:
            print('FAILED ---> Long Vs Shorts database did not save!')

    def call_all_long_vs_short(self):

        url = ['BTC', 'ETH', 'LINK', 'USDT']
        for items in url:
            data = self.get_coinglass_long_vs_short(items)
            db_list = self.filter_long_vs_short(data, items)
            self.upload_long_vs_short(db_list)
            sleep(4)





# url = ['BTC', 'ETH', 'LINK', 'USDT']
# test = Get_CoinGlass_Longs_VS_Shorts()
# db_test = CoinGlass_DB()
# for items in url:
#     data = test.get_coinglass_long_vs_short(items)
#     test.filter_long_vs_short(data, items)
#     sleep(4)



