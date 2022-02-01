from requests_html import HTMLSession
import json
from coin_glas_db import CoinGlass_DB

class Get_BitcoinBubble_Coin_Glass:
    """This class set's up the session and the get info"""

    def __init__(self):
        self.sessions = HTMLSession()
        self.header = {'coinglassSecret': 'c98d6aedfd05401cb87a38125c3e5555'}
        self.params = {}
        self.base_url = "https://fapi.coinglass.com/api/index/bitcoinBubbleIndex"


    def get_bb_index_coinglass(self):
        """"""
        self.r = self.sessions.get(self.base_url, headers=self.header, data=self.params)
        api_data = self.r.html.html
        print(self.r)
        data = json.loads(api_data)

        return data

    def filter_data_upload(self, data):
        """Going to filter the data to remove some key in the dic and turn into list"""
        db_list=[]

        all_bubble_data = data['data']
        for bubble_data in all_bubble_data:
            del bubble_data['c']
            del bubble_data['hotKey']
            values = list(bubble_data.values())
            db_list.append(values)

        for x in db_list:
            print(x)

        if len(db_list) < 1:
            print('FAILED ---> Bitcoin Bubble Index database did not save!')
        CoinGlass_DB.insert_bitcoin_bubble_index(db_test, id_list=db_list)





test = Get_BitcoinBubble_Coin_Glass()
db_test = CoinGlass_DB()
data = test.get_bb_index_coinglass()
test.filter_data_upload(data)