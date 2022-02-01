from db_config import DB_Config

class Sentiment_DB(DB_Config):
    """crypto_sentiment <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)

    def insert_fear_greed_index(self, id_list):
        """Writing SQL to DB with a single value method called"""
        sql = """
        INSERT INTO `fear_greed_index`(`value`, `value_classification`, `date_time`)
        VALUES (%s, %s, FROM_UNIXTIME(%s))
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)




