from time import sleep
from on_chain.on_chain_db import OnChain_DB

class Get_100_top_Wallets_Data(OnChain_DB):

    def get_100_top_wallets(self):
        self.base_url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses.html'
        self.r = self.sessions.get(self.base_url, headers=self.header)
        print(self.r, 'Getting top 100 crypto wallets')
        # Want to separate the exchange wallets from the individual wallets
        db_none_exchange = []
        db_exchange = []
        raw_data = self.r.html.find('tr')
        for x in raw_data[14:]:
            x = x.text.split('\n')
            if 'wallet' in x[2]:
                x[3] = x[3][:x[3].find('BTC')]
                x = x[:4]
                db_exchange.append(x)
            else:
                 x[2] = x[2][:x[2].find('BTC')]
                 x = x[:3]
                 db_none_exchange.append(x)

        # displaying information in terminal (mainly for testing)
        for x in db_none_exchange:
            print(x)
        print('')
        for x in db_exchange:
            print(x)

        return db_none_exchange, db_exchange

    def upload_wallets(self, db_none_exchange, db_exchange):
        # Uploading both lists to two different tables in same DB
        self.insert_top_btc_wallets_none_exchange(id_list=db_none_exchange)
        sleep(4)
        self.insert_top_btc_wallets_exchange(id_list=db_exchange)


    def call_all_richest_wallets(self):
        db_none_exchange, db_exchange = Get_100_top_Wallets_Data.get_100_top_wallets(self)
        self.upload_wallets(db_none_exchange, db_exchange)



# test = Get_100_top_Wallets_Data('crypto_onchain_db')
# # db_test = OnChain_DB()
# test.get_100_top_wallets()