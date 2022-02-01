import json
from coin_glass.coin_glas_db import CoinGlass_DB

class Get_BitcoinBubble_Coin_Glass(CoinGlass_DB):

    def get_btc_options_oi(self):
        """"""
        self.base_url = "https://fapi.coinglass.com/api/option/statisticsAndChart?symbol=BTC&timeType=0&currency=USD"
        self.r = self.sessions.get(self.base_url, headers=self.coinglass_header, data=self.params)
        api_data = self.r.html.html
        print(self.r, 'CoinGlass Options Open Interest')
        raw_data = json.loads(api_data)
        # print(raw_data)
        return raw_data


    def filter_btc_options_oi(self, data):

        date_list = data['data']['chart'][0]['dateList']
        price_list = data['data']['chart'][0]['priceList']
        deribit_exchange_list = data['data']['chart'][0]['dataMap']['Deribit']
        ledgerx = data['data']['chart'][0]['dataMap']['LedgerX']
        ftx = data['data']['chart'][0]['dataMap']['FTX']
        cme = data['data']['chart'][0]['dataMap']['CME']
        # print(len(date_list))
        db_list = []
        for (a, b ,c ,d ,e ,f ) in zip(date_list, price_list, deribit_exchange_list, ledgerx, ftx, cme):
            a = (str(a / 1000), str(b) ,str(c) ,str(d) ,str(e) ,str(f) )
            a = list(a)
            db_list.append(a)
        #
        # for x in db_list:
        #     print(x)
        # print('')
        print(db_list[-1])

        return db_list[-1]

    def upload_options_oi(self, db_list):

        checker = self.insert_bitcoin_options_oi(id_list=db_list)
        if checker == False:
            print('FAILED ---> Bitcoin options OI database did not save!')

    def call_all_ptions_oi(self):
        data = self.get_btc_options_oi()
        db_list = self.filter_btc_options_oi(data)
        self.upload_options_oi(db_list)


# test = Get_BitcoinBubble_Coin_Glass('crypto_coin_glass_db')
# test.call_all_ptions_oi()
