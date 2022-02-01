import json
from coin_glass.coin_glas_db import CoinGlass_DB

class Get_CoinGlass_funding(CoinGlass_DB):

    def get_coinglass_funding(self):
        self.base_url = 'https://fapi.coinglass.com/api/fundingRate/v2/home'
        self.r = self.sessions.get(self.base_url, headers=self.coinglass_header, data=self.params)
        print(self.r, 'CoinGlass Funding Rate')
        api_data = self.r.text.encode('utf8')
        raw_data = json.loads(api_data)
        return raw_data

    def filter_funding_data(self, raw_data):
        coins = ['BTC', 'ETH', 'LINK']
        complete_list = []
        for x in raw_data['data']:
            if x['symbol'] in coins:
                # print(x)
                # print(x['symbol'])
                rates = []
                rates.append(x['symbol'])
                try:
                    for items in x['uMarginList']:
                        # print(items['rate'])
                        rates.append(items['rate'])
                    for items in x['cMarginList']:
                        # print(items['rate'])
                        rates.append(items['rate'])
                except KeyError:
                    rates.append('Null')
                while len(rates) < 14:
                    rates.append('Null')
                complete_list.append(rates)
                del rates

        for items in complete_list:
            print(items)
            print(len(items))

        return complete_list

    def upload_funding_rate_coinglass(self, complete_list):
        checker = self.insert_funding_rates(id_list=complete_list)
        if checker == False:
            print('FAILED ---> CoinGlass Open Interest database did not save!')


    def call_all_funding_rate(self):

        data = self.get_coinglass_funding()
        complete_list = self.filter_funding_data(data)
        self.upload_funding_rate_coinglass(complete_list)




# test = Get_CoinGlass_funding()
# db_test = CoinGlass_DB()
# data = test.get_coinglass_funding()
# test.filter_funding_data(data)