from db_config import DB_Config

class ViewBase_DB(DB_Config):
    """'Crypto_Scraping' <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)


    def insert_exchange_flow(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `exchange_flow_viewbase`(`id`, `ticker`, `supply_on_exchange`,
        `supply_on_exchange_percentage`, `1d_change`, `1d_change_usd`, `1d_change_percentage`,
        `7d_change`, `7d_change_usd`, `7d_change_percentage`, `30d_change`, `30d_change_usd`,
        `30d_change_percentage`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_futures_liquidations_viewbase(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `futures_liquidations_viewbase`(`ticker`, `long_liquidations(24hr)`,
        `short_liquidations(24hr)`, `total_liquidations(24hr)`)
        VALUES (%s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

        # RISK FOUND IF THE RESULT IS -1 OR BELOW 1 THEN
        # SEND EMAIL SAYING THERE WERE NO UPDATES FOR WHAT EVER REASON??

    def insert_open_intrest_viewbase(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `open_intrest_viewbase`(`ticker`, `total_oi`, `oi_change_24hr`,
        `oi_percent_change_24hr`, `price_percent_change_24hr`)
        VALUES (%s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

    def insert_funding_viewbase(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `funding_viewbase`(`ticker`, `binance_usd`, `ftx_usd`, 
        `hubio_usd`, `okex_usd`, `bybit_usd`, `binance_coin`, `ftx_coin`, `hubio_coin`, 
        `okex_coin`, `bybit_coin`, `deribit`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

    def insert_top_futures_traders_position(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `futures_traders_position`(`ticker`, `binance_usd_perp`, 
        `binance_coin_perp`, `huobi_coin_perp`, `huobi_coin_futures`)
        VALUES (%s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

    def insert_margin_interest_ratesn(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `margin_interest_rates`(`ticker`, `binance`, `okex`)
        VALUES (%s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_bitfinex_margin_total_long_short_viewbase(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `bitfinex_margin_total_long_short_viewbase`(`ticker`, `long_posistion`, 
        `24hr_change_long`, `short_posistion`, `24hr_change_short`, `percent_long_vs_short`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)



