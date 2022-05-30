from time import sleep
from exchange_balance.viewbase_db import ViewBase_DB
import ast


class Get_Exchange_History(ViewBase_DB):

    def get_exchange_history(self):

        # urls = ['bitcoin', 'ethereum', 'tether', 'usd-coin', 'chainlink']
        urls = {'bitcoin':'BTC', 'ethereum':'ETH', 'tether':'USDT', 'usd-coin':'USDC', 'chainlink':'LINK'}
        for url in urls:
            base_url = f'https://www.viewbase.com/coin/{url}'
            r = self.sessions.get(base_url, headers=self.header)
            # print(r)
            doc = r.html.html
            start_doc = doc.find('var combinedData')
            end_doc = doc.find('var seriesArray ')
            # print(start_doc, end_doc)
            doc = doc[start_doc + 27:end_doc - 18]
            doc = doc.replace('null,', '')

            mylist = ast.literal_eval(doc)

            upload_list2 = []

            upload_list2.append(mylist[-1][0] / 1000)
            upload_list2.append(sum(mylist[-1][4:]))
            upload_list2.append(urls[url])

            print(upload_list2)
            self.insert_exchange_history(upload_list2)
            sleep(1)




            #
            # upload_list2 = []
            # for items in mylist:
            #     print(items)
            #     upload_list = []
            #     upload_list.append(items[0] / 1000 )
            #     total = sum(items[4:])
            #     upload_list.append(total)
            #     upload_list.append(urls[url])
            #     upload_list2.append(upload_list)
            # print(upload_list2)
            # self.insert_exchange_history(upload_list2)
            # sleep(4)


#
#
# test = Get_Exchange_History('Crypto_Scraping')
# test.get_exchange_history()