import pyppeteer.errors
from time import sleep
from email_config import sendingemail
from exchange_balance.viewbase_db import ViewBase_DB


class Get_Crypto_Balance(ViewBase_DB):
    counter = 1
    def get_data(self, url, delay):
        self.base_url = 'https://www.viewbase.com/'
        self.coins_to_follow = ['BTC', 'ETH', 'USDT', 'USDC', 'LINK']
        try:
            r = self.sessions.get(self.base_url + url, headers=self.header)
            print(r, 'ViewBase, Getting ', url, 'data')
            r.html.render(sleep=delay, timeout=delay)
        except pyppeteer.errors.TimeoutError as err:
            print(err)
            sendingemail(f'{err} +  for getting {self.base_url} + {url}', 'Viewbase Get Error')

        if url == 'exchange':
            self.get_data_exchange_flow(r)
        if url == 'liquidation':
            self.get_liquidations(r)
        if url == 'futures':
            self.get_open_interest(r)
        if url == 'funding':
            self.get_funding(r)
        if url == 'long_short_position':
            self.get_top_futures_traders_position(r)
        if url == 'margin':
            self.get_margin_interest_rates(r)
        if url == 'bitfinex_long_short_position':
            self.get_bitfinex_margin_total_long_short_viewbase(r)


    def get_data_exchange_flow(self, r):
        """exchange"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr.exchange_overview_row')
        for balance_data in balance_datas:
            balance_data = str(balance_data.text).split('\n')
            if balance_data[1] in self.coins_to_follow:
                balance_data[0] = None
                flow_exchange_list.append(balance_data)
        for items in flow_exchange_list:
            print(items)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Exchange database did not save!')
            else:
                print('FAILED ---> Exchange database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('exchange', 140)
        else:
            self.insert_exchange_flow(id_list=flow_exchange_list)


    def get_liquidations(self, r):
        """liquidation"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr.oi_overview_row')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[1] in self.coins_to_follow:
                flow_exchange_list.append(items[1:5])
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Liquidation database did not save!')
            else:
                print('FAILED ---> Liquidation database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('liquidation', 140)
        else:
            self.insert_futures_liquidations_viewbase(id_list=flow_exchange_list)

    def get_open_interest(self, r):
        """futures"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr.oi_overview_row')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[1] in self.coins_to_follow:
                flow_exchange_list.append(items[1:6])
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Futures database did not save!')
            else:
                print('FAILED ---> Futures database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('futures', 140)
        else:
            self.insert_open_intrest_viewbase(id_list=flow_exchange_list)

    def get_funding(self, r):
        """funding"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr[role]')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[1] in self.coins_to_follow:
                flow_exchange_list.append(items[1:])
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Futures database did not save!')
            else:
                print('FAILED ---> Futures database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('funding', 140)
        else:
            self.insert_funding_viewbase(id_list=flow_exchange_list)

    def get_top_futures_traders_position(self, r):
        """long_short_position"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[1] in self.coins_to_follow:
                flow_exchange_list.append(items[1:])
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Long_Short_Position database did not save!')
            else:
                print('FAILED ---> Long_Short_Position database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('long_short_position', 140)
        else:
            self.insert_top_futures_traders_position( id_list=flow_exchange_list)


    def get_margin_interest_rates(self, r):
        """margin"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[0] in self.coins_to_follow:
                flow_exchange_list.append(items)
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Margin database did not save!')
            else:
                print('FAILED ---> Margin database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('margin', 140)
        else:
            self.insert_margin_interest_ratesn(id_list=flow_exchange_list)

    def get_bitfinex_margin_total_long_short_viewbase(self, r):
        """bitfinex_long_short_position"""
        flow_exchange_list = []
        balance_datas = r.html.find('tr')
        for items in balance_datas:
            items = items.text.split('\n')
            if items[0][:3] in self.coins_to_follow:
                flow_exchange_list.append(items)
            if items[0][:4] in self.coins_to_follow:
                flow_exchange_list.append(items)
        for x in flow_exchange_list:
            print(x)
        if len(flow_exchange_list) < 1:
            if Get_Crypto_Balance.counter == 5:
                sendingemail('FAILED ---> Bitfinex_Long_Short_Position database did not save!')
            else:
                print('FAILED ---> Bitfinex_Long_Short_Position database did not save!')
                Get_Crypto_Balance.counter = Get_Crypto_Balance.counter + 1
                print(Get_Crypto_Balance.counter)
                self.get_data('bitfinex_long_short_position', 140)
        else:
            self.insert_bitfinex_margin_total_long_short_viewbase(id_list=flow_exchange_list)

    def call_all_viewbase(self):

        pages = ['exchange', 'liquidation', 'futures', 'funding',
                 'long_short_position', 'margin', 'bitfinex_long_short_position']

        for page in pages:
            self.get_data(page, 70)
            sleep(10)
            Get_Crypto_Balance.counter = 0
        print('Done')


#TODO is to re write this code and to have the loop send a new R request for each function (will reduce code)

test = Get_Crypto_Balance('Crypto_Scraping')
test.call_all_viewbase()

# test.get_data('futures', 5)