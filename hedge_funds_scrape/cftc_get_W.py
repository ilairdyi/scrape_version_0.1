from hedge_funds_scrape import hedge_fund_db
import pyppeteer.errors
import time

class Get_CFTC_Data(hedge_fund_db.Hedge_Funds_DB):

    def get_cftc_data(self):
        self.base_url = 'https://www.cftc.gov/dea/futures/financial_lf.htm'
        try:
            self.r = self.sessions.get(self.base_url, headers=self.header)
        except pyppeteer.errors.TimeoutError as err:
            print(err)
        else:
            print(self.r, 'Getting CFTC Data weekly')
            # r.html.render(sleep=2, timeout=2)

    def filter_cftc_data(self):
        products = ['BITCOIN - CHICAGO MERCANTILE EXCHANGE   (5 Bitcoins)  ',
                    'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE   (Bitcoin X $0.10)',
                    'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE   (50 Index Points)',
                    'MICRO ETHER  - CHICAGO MERCANTILE EXCHANGE   (0.1 Index Points)   '
                    ]

        # db_list = [
        #     'cftc_bitcoin', 'cftc_micro_bitcoin', 'cftc_ether', 'cftc_micro_ether'
        # ]

        for product in products:
            doc = self.r.html.html
            btc_doc = doc.find(product)
            end_btc_doc = doc.find('U.S. DOLLAR INDEX - ICE FUTURES U.S.   (U.S. DOLLAR INDEX X $1000)')
            doc = doc[btc_doc:end_btc_doc]
            doc = doc.split('\n')

            new_list = []
            for items in (doc[:14]):
                test = (" ".join(items.split()))
                test = test.split(' ')
                new_list.append(test)

            complete_list = []

            a = 'Current ' + new_list[2][0]
            b = new_list[3]
            c = new_list[1][-1]
            b.insert(0, a)
            b.append(c)
            # print(b)

            a2 = new_list[5][0] + '  From last week'
            b2 = new_list[6]
            c2 = new_list[5][-1]
            b2.insert(0, a2)
            b2.append(c2)
            # print(b2)

            a3 = new_list[8][0] + ' of OI each category '
            b3 = new_list[9]
            c3 = 'NA'
            b3.insert(0, a3)
            b3.append(c3)
            # print(b3)

            a4 = new_list[11][0] + ' of Traders in Each Category'
            b4 = new_list[12]
            b4_part2 = '.'
            c4 = new_list[11][-1]
            b4.insert(0, a4)
            b4.append(b4_part2)
            b4.append(b4_part2)
            b4.append(c4)
            # print(b4)

            complete_list.append(b)
            complete_list.append(b2)
            complete_list.append(b3)
            complete_list.append(b4)

            print(product)
            if product == 'BITCOIN - CHICAGO MERCANTILE EXCHANGE   (5 Bitcoins)  ':
                db_name = '`cftc_bitcoin`'
                self.insert_cftc_data(db_name, complete_list)
                for x in complete_list:
                    print(x)
            time.sleep(1)
            if product == 'MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE   (Bitcoin X $0.10)':
                db_name = 'cftc_micro_bitcoin'
                self.insert_cftc_data(db_name, complete_list)
                for x in complete_list:
                    print(x)
            time.sleep(1)
            if product == 'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE   (50 Index Points)':
                db_name = 'cftc_ether'
                self.insert_cftc_data(db_name, complete_list)
                for x in complete_list:
                    print(x)
            time.sleep(1)
            if product == 'MICRO ETHER  - CHICAGO MERCANTILE EXCHANGE   (0.1 Index Points)   ':
                db_name = 'cftc_micro_ether'
                self.insert_cftc_data(db_name, complete_list)
                for x in complete_list:
                    print(x)
            time.sleep(1)
            print('')

    def call_all_cftc(self):
        self.get_cftc_data()
        self.filter_cftc_data()




#
# test = Get_CFTC_Data('crypto_hedge_funds_db')
# # db_test = ViewBase_DB()
# test.get_cftc_data()
# test.filter_cftc_data()