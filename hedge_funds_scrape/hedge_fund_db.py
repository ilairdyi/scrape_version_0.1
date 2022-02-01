from db_config import DB_Config

class Hedge_Funds_DB(DB_Config):
    """'crypto_hedge_funds_db' <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)

    def insert_cme_oi_volume(self, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = """
        INSERT INTO `cme_oi_volume`(`product_name`, `cleared_as`, `volume`, `open_interest`)
        VALUES (%s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

    def insert_cftc_data(self, table_name, id_list):
        """Will just deal with inserting into exchange flow table"""
        sql = f"""
        INSERT INTO {table_name}(`type`, `dealer_long`, `dealer_short`, 
        `dealer_spreading`, `institutional_long`, `institutional_short`, `institutional_spreading`, 
        `leveraged_long`, `leveraged_short`, `leveraged_spreading`, `other_reports_long`, `other_reports_short`, 
        `other_reports_spreading`, `nonreportable_long`, `nonreportable_short`, `total`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.executemany(sql, list_of_records)

