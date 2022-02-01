from requests_html import HTMLSession
import pyppeteer.errors
import json
from coin_glas_db import CoinGlass_DB


class Get_BBTC_Treasuries_Coin_Glass:
    """This class set's up the session and the get info"""

    def __init__(self):
        self.sessions = HTMLSession()
        self.header = {'coinglassSecret': 'c98d6aedfd05401cb87a38125c3e5555'}
        self.params = {}
        self.base_url = "https://fapi.coinglass.com/api/bitcoinTreasuries"


    def get_btc_treasuries(self):
        """"""
        self.r = self.sessions.get(self.base_url, headers=self.header, data=self.params)
        api_data = self.r.html.html
        print(self.r)
        raw_data = json.loads(api_data)
        # print(raw_data)

        return raw_data

    def filter_btc_treasuries(self, raw_data):

        db_list = []
        for x in raw_data['data']:
            for j in raw_data['data'][x]:
                a = (j['companyName'], j['amount'], x)
                a = list(a)
                db_list.append(a)

        for x in db_list:
            print(x)

        checker = CoinGlass_DB.insert_btc_treasuries(db_test, id_list=db_list)
        if checker == False:
            print('FAILED ---> Bitcoin Bubble Index database did not save!')




test = Get_BBTC_Treasuries_Coin_Glass()
db_test = CoinGlass_DB()
data = test.get_btc_treasuries()
test.filter_btc_treasuries(data)