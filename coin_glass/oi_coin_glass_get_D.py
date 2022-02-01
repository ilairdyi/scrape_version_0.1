import json
from time import sleep
from coin_glass.coin_glas_db import CoinGlass_DB

class Get_Coin_Glass(CoinGlass_DB):

    def get_oi_api_coinglass(self, symbol):
        """"""
        self.base_url = "http://open-api.coinglass.com/api/pro/v1/futures/openInterest?interval=12H&symbol="
        db_list = []
        self.r = self.sessions.get(self.base_url + symbol, headers=self.coinglass_header, data=self.params)
        api_data = self.r.text.encode('utf8')
        data = json.loads(api_data)
        data = data['data'][0]
        data.pop('exchangeName')
        data['openInterest'] = int(data['openInterest'])
        data['openInterestAmount'] = int(data['openInterestAmount'])
        data['volUsd'] = int(data['volUsd'])
        data['avgFundingRate'] = format(data['avgFundingRate'], ".3f")
        # print(data)
        for x in data:
            db_list.append(data[x])
        print(db_list)

        return db_list

    def upload_db(self, upload_to_db):
        checker = self.insert_oi_coin_glass(id_list=upload_to_db)
        if checker == False:
            print('FAILED ---> CoinGlass Open Interest database did not save!')
            # TODO think of some kind of back up failer thing

    def call_all_oi_coinglass(self):
        coins = ['BTC', 'ETH', 'LINK', 'USDT']
        upload_to_db = []
        for items in coins:
            db_list = self.get_oi_api_coinglass(items)
            sleep(2)
            upload_to_db.append(db_list)

        self.upload_db(upload_to_db)


# test = Get_Coin_Glass()
# db_test = CoinGlass_DB ()
# upload_to_db = []
#
# for items in coins:
#     db_list = test.get_oi_api_coinglass(items)
#     sleep(2)
#     upload_to_db.append(db_list)
#
# test.upload_db(upload_to_db)