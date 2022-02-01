import mysql.connector
import socket
from requests_html import HTMLSession

class DB_Config():

    def __init__(self, database):
        # all param for Get requests to websites
        self.sessions = HTMLSession()
        self.header = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
        # CoinGlass API
        self.coinglass_header = {'coinglassSecret': 'c98d6aedfd05401cb87a38125c3e5555'}
        self.params = {}
        self.checker = True

        #Would use socket to require my current IP for rasberry
        hostname = socket.gethostname()
        # local_ip = socket.gethostbyname(hostname)
        local_ip = '192.168.1.175'
        # print(local_ip)

        # Config setting for connecting to myphpadmin database
        self.user = 'pitest'
        self.password = 'Poshsheep'
        self.host = local_ip
        self.database = database
        self.port = 3306
        try:
            self.mydb =  mysql.connector.connect(user=self.user,
                                             password=self.password,
                                             host=self.host,
                                             database=self.database,
                                             port=self.port)

            self.mycursor = self.mydb.cursor()
            print(f'Success to connecting to your database --> {self.database}')
        except mysql.connector.Error as err:
            print(err)

    # These functions set query to my DB either single or multiple inputs
    def executemany(self, sql, list_of_records):
        self.mycursor.executemany(sql, list_of_records)
        #self.mydb.commit()
        print(self.mycursor.rowcount, 'rows have been added')
        if self.mycursor.rowcount <= 0:
            print('FAILED')

    def single_excute(self, sql, list_of_records):
        self.mycursor.execute(sql, list_of_records)
        #self.mydb.commit()
        print(self.mycursor.rowcount, 'rows have been added')
        if self.mycursor.rowcount < 0:
            print('FAILED')




