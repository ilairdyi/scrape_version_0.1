from db_config import DB_Config

class Marketcaps_DB(DB_Config):

    def __init__(self, database):
        DB_Config.__init__(self, database)

    def insert_price_vol_coingeckco(self, id_list):
        sql = """
        INSERT INTO `price_vol_coingeckco`(`ticker`, `date_time`, `price`, `volume_usd`)
        VALUES (%s, FROM_UNIXTIME(%s), %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)


    def insert_coingeckco_overall_stats(self, id_list):
        sql = """
         INSERT INTO `gecko_overall`(`amount_cryptos`, `amount_exchanges`, `market_cap`, 
         `%_change of market_cap`, `24hr_vol`, `btc_dom`, `eth_dom`, `eth_gas`)
         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
         """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)
