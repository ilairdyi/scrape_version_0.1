from db_config import DB_Config

class CoinGlass_DB(DB_Config):
    """'crypto_coin_glass_db' <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)

    def insert_oi_coin_glass(self, id_list):
        sql = """
        INSERT INTO `oi_coin_glass`(`ticker`, `oi_usd`, `oi_in_btc`, `vol_in_usd`, `h24_change`, 
        `rate`, `vol_change_percent`, `h1_oi_change_percent`, `h4_oi_change_percent`, `avg_funding_rate`, 
        `oi_change_percent`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_bitcoin_bubble_index(self, id_list):
        sql = """
        INSERT INTO `bitcoin_bubble_index_coinglass`(`bitcoin_tweets`, `bitcoin_difficulty`, 
        `bitcoin_sent_by_address`, `bitcoin_price`, `bubble_index`,`date_time`, 
        `bitcoin_google_trends`, `bitcoin_transactions`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_bitcoin_options_oi(self, id_list):
        sql = """
        INSERT INTO `btc_options_open_interest`(`date_time`, `price`, `deribit`, `ledgerx`, `ftx`, `cme`)
        VALUES (FROM_UNIXTIME(%s), %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)


    def insert_grayscale_holdings(self, id_list):
        sql = """
        INSERT INTO `grayscale_holdings`(`ticker`, `holdings`, `price`, `date_time`)
        VALUES (%s, %s, %s, FROM_UNIXTIME(%s))
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)

    def insert_funding_rates(self, id_list):
        sql = """
        INSERT INTO `funding_coinglass`(`ticker`, `binance_usd`, `okex_usd`, 
        `bybit_usd`, `ftx_usd`, `dydx_usd`, `gate_usd`, `bitget`, `binance_coin`, `okex_coin`, 
        `bybit_coin`, `bitmex_coin`, `huobi`, `deribit`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)


    def insert_liquidations(self, id_list):
        sql = """
        INSERT INTO `liquidation_data_coinglass`(`ticker`, `amount_in_assest`, `long_vol_usd`, 
        `short_vol_usd`, `total_vol_usd`)
        VALUES (%s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

    def insert_longs_vs_shorts(self, id_list):
        sql = """
        INSERT INTO `long_vs_shorts_coinglass`(`ticker`, `long_percentage`, 
        `short_percentage`, `price`, `long_short_ratio`, `date_time`)
        VALUES (%s, %s, %s, %s, %s, FROM_UNIXTIME(%s))
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)


    def insert_exchange_flows(self, id_list):
        sql = """
        INSERT INTO `exchange_flow_coinglass`(`huobi`, `coincheck`, `kraken`, `binance`, 
        `coinbase_pro`, `gate`, `okex`, `poloniex`, `bitflyer`, `bitfinex`, `bitstamp`, `bittrex`, 
        `total_balance`, `datelist`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s))
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)


    def insert_btc_treasuries(self, id_list):
        sql = """
        INSERT INTO `btc_treasuries`(`company_name`, `amount_btc`, `entity_type`)
        VALUES (%s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)
