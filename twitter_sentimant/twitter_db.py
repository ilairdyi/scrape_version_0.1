from db_config import DB_Config

class Twitter_Senitment_DB(DB_Config):
    """crypto_twitter_sentiment <--- is the database were trying to connect to"""

    def __init__(self, database):
        DB_Config.__init__(self, database)

    def insert_total_pol_sub(self, id_list):
        """Writing SQL to DB with a single value method called"""
        sql = """
        INSERT INTO `total_pol_sub`(`Positive`, `Netural`, `Negative`, `Opinionated`, `Mixed`, `Factual`)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)

    def insert_polairty_with_subjectivity_results(self, id_list):
        """Writing SQL to DB with a single value method called"""
        sql = """
        INSERT INTO `polairty_with_subjectivity_results`(`pos-opinionated`, `pos-mixed`, `pos-factual`, 
        `netural-opinionated`, `netural-mixed`, `netural-factual`, `neg-opinionated`, `neg-mixed`, `neg-factual`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        list_of_records = [each for each in id_list]
        self.single_excute(sql, list_of_records)

    def insert_twitter_key_words(self, id_list):
        sql = """
         INSERT INTO `twitter_key_words`(`words`, `total_count`) 
         VALUES (%s, %s)
         """
        for key, val in id_list.items():
            a = (key, val)
            self.mycursor.execute(sql, a)
        self.mydb.commit()

    def get_twitter_id_dates(self):
        self.mycursor.execute("SELECT * FROM `twitter_checker`")
        myresult = self.mycursor.fetchall()
        return myresult

    def insert_twitter_checker_db(self, id_list):
        #Here we are adding to the checker table
        sql = """
        INSERT INTO `twitter_checker`(`twitter_dates`, `twitter_id`)
        VALUES (%s, %s)
        """
        list_of_records = [each for each in id_list]
        self.mycursor.executemany(sql, list_of_records)
        self.mydb.commit()
        print(self.mycursor.rowcount, 'rows have been added to twitter checker db')


