from marketcap_sites.marketcaps_db import Marketcaps_DB

class Get_Overallstats_Coin_Gecko(Marketcaps_DB):

    def get_overall_data(self):
        """"""
        self.base_url = 'https://www.coingecko.com/en/overall_stats'
        self.r = self.sessions.get(self.base_url, headers=self.header)
        print(self.r, 'Getting CoinGecko Overall Data')
        data = self.r.html.find('div')
        data = data[0].text.replace(' ', 'x').replace('\n', 'x')
        data = data.split('x')
        # data[18] had to be changed FROM data[20]
        data = data[1], data[4], data[7], data[8], data[11], data[14], data[16], data[18]
        data = list(data)
        print(data)
        return data

    def upload_db(self, data):
        self.insert_coingeckco_overall_stats(id_list=data)

    def call_all(self):
        data = self.get_overall_data()
        self.upload_db(data)



# test = Get_Price_Vol_Coin_Gecko()
# db_test = Marketcaps_DB()
# test.get_overall_data()
