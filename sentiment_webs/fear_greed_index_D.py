import json
from sentiment_webs.sentiment_db import Sentiment_DB

class Get_Fear_Greed_index(Sentiment_DB):

    def get_fear_greed_index(self):
        # Collecting data from website and returning unfiltered data
        self.base_url = 'https://api.alternative.me/fng/'
        self.r = self.sessions.get(self.base_url, headers=self.header)
        api_data = self.r.html.html
        print(self.r, 'Fear and Greed Index')
        raw_data = json.loads(api_data)
        # print(raw_data)
        return raw_data

    def filter_fear_greed_index(self, raw_data):
        #Once the data is in the list all want is the last value
        data = list(raw_data['data'][0].values())
        del data[-1]
        return data

    def db_upload(self, data):
        #uplaoding data to DB
        self.insert_fear_greed_index(id_list=data)

    def call_all(self):
        #Function that calls all other functions
        data = self.get_fear_greed_index()
        db_data = self.filter_fear_greed_index(data)
        print(db_data)
        self.db_upload(db_data)


    # USE for taking large amoutn of data
    #     db_list = []
    #     for x in raw_data['data']:
    #         x = list(x.values())
    #         db_list.append(x)
    #     db_list.reverse()
    #     del db_list[-1][3]
    #     for x in db_list:
    #         print(x)
    # #


# test = Get_Fear_Greed_index()
# # db_test = DB_Config('crypto_sentiment')
# db_test = Sentiment_DB('crypto_sentiment')
#
# data = test.get_fear_greed_index()
# test.filter_fear_greed_index(data)
