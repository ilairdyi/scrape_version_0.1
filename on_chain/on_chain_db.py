from db_config import DB_Config

class OnChain_DB(DB_Config):
    """'crypto_onchain_db' <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)


    def insert_top_btc_wallets_none_exchange(self, id_list):
        sql = """
        INSERT INTO `top_btc_wallets_none_exchange_bitinfocharts`(`rank`, `address`, `amount_btc`)
        VALUES (%s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_top_btc_wallets_exchange(self, id_list):
        sql = """
        INSERT INTO `exchange_wallets_bitinfocharts`(`rank`, `address`, `exchange`, `amount_btc`)
        VALUES (%s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)
