import pyppeteer.errors
from hedge_funds_scrape.hedge_fund_db import Hedge_Funds_DB

class Get_CME_Data(Hedge_Funds_DB):

    def get_cme_data(self):
        self.base_url = 'https://www.cmegroup.com/trading/micro-bitcoin-futures.html#trading'
        try:
            self.r = self.sessions.get(self.base_url, headers=self.header)
        except pyppeteer.errors.TimeoutError as err:
            print(err)
        else:
            print(self.r, 'Getting CME data')

    def filter_cme_data(self):

        data_collection = self.r.html.find('tr.null')
        open_interest_list = []
        for items in data_collection:
            items = items.text.split('\n')
            part_items_a = items[-3:]
            part_items_b = items[4]
            part_items_a.insert(0, part_items_b)
            open_interest_list.append(part_items_a)
        for x in open_interest_list:
            print(x)

        return open_interest_list

    def upload_cme_data(self, data):
        self.insert_cme_oi_volume(data)

    def call_all_cme(self):
        self.get_cme_data()
        data = self.filter_cme_data()
        self.upload_cme_data(data)


#
# test = Get_CME_Data('crypto_hedge_funds_db')
# test.get_cme_data()
# test.filter_cme_data()