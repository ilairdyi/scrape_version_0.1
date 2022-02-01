import json
from coin_glass.coin_glas_db import CoinGlass_DB

class Get_CoinGlass_Liquidations(CoinGlass_DB):

    def get_coinglass_liquidations(self):
        self.base_url = 'https://fapi.coinglass.com/api/futures/liquidation/info?symbol=&timeType=5&size=12'
        self.r = self.sessions.get(self.base_url, headers=self.coinglass_header, data=self.params)
        print(self.r, 'CoinGlass Amount of Liquidations')
        api_data = self.r.text.encode('utf8')
        raw_data = json.loads(api_data)
        # print(raw_data)
        return raw_data

    def filter_liquidations(self, data):
        coins = ['BTC', 'ETH', 'LINK', 'USDT', 'USDC']
        db_list = []

        if data['data']['ex'][0]['exchangeName'] == 'All':
            total_liquidations = data['data']['ex'][0]
            del total_liquidations['number']
            del total_liquidations['rate']
            del total_liquidations['exchangeLogo']
            del total_liquidations['shortRate']
            del total_liquidations['longRate']
            total_liquidations = (total_liquidations['exchangeName'], total_liquidations['averagePrice'],
                                      total_liquidations['longVolUsd'],total_liquidations['shortVolUsd'],
                                      total_liquidations['totalVolUsd'])
            total_liquidations = list(total_liquidations)
            db_list.append(total_liquidations)

        for items in data['data']['coin']:
            if items['symbol'] in coins:
                del items['number']
                del items['symbolLogo']
                x = list(items.values())
                db_list.append(x)

        for x in db_list:
            print(x)

        return db_list

    def upload_liquidations_coinglass(self, db_list):
        checker = self.insert_liquidations( id_list=db_list)
        if checker == False:
            print('FAILED ---> CoinGlass liquidations database did not save!')

    def call_all_liquidations_coinglass(self):
        data = self.get_coinglass_liquidations()
        db_list = self.filter_liquidations(data)
        self.upload_liquidations_coinglass(db_list)




# test = Get_CoinGlass_Liquidations()
# db_test = CoinGlass_DB()
# data = test.get_coinglass_liquidations()
# test.filter_liquidations(data)

