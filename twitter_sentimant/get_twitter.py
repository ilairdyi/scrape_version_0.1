import re
import tweepy
import textblob
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
import spacy
nlp = spacy.load('en_core_web_lg')
from twitter_sentimant.twitter_db import Twitter_Senitment_DB
from time import sleep
import os

class Get_Twitter_Sentiment(Twitter_Senitment_DB):

    def api_keys(self):
        """Getting my APi keys"""
        path = os.path.abspath(os.path.dirname(__file__))
        # print(path)

        with open(path + '\details.txt', 'r') as all_keys:
            #must use this way to get rid of the \n
            all_keys = all_keys.read().splitlines()

        consumer_key = all_keys[1]
        consumer_secret = all_keys[3]
        access_token = all_keys[5]
        access_token_secret = all_keys[7]

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        except:
            print("Error: Authentication Failed")
        else:
            print('Success to access twitters API, now fetching data')

    def get_db_twitter_ids_dates(self):
        myresults = Twitter_Senitment_DB.get_twitter_id_dates(self)
        db_twitter_date = []
        db_twitter_id = []
        for x in myresults:
            a, b = x
            db_twitter_date.append(a)
            db_twitter_id.append(b)

        return db_twitter_date, db_twitter_id


    def get_tweets(self,db_twitter_date, db_twitter_id):
        """Search for our key word and send query through to twitter API"""
        # Key search term
        topic = 'Bitcoin'
        # This will help stop search for retweets(dont work tho)
        search = f'#{topic} -filter:retweets'
        # This method will search any tweets with our key search term word
        tweet_cursor = tweepy.Cursor(self.api.search_tweets, q=search, lang='en', tweet_mode="extended").items(200)

        #Great for search a cetain person like eleon musk
        # tweet_cursor = self.api.user_timeline(screen_name="ElonMusk", count=5, tweet_mode="extended")
        # text = json.loads(tweet_cursor)

        tweet_dates = []
        tweet_text = []
        tweet_ids = []

        for tweet in tweet_cursor:
            twt_id = str(tweet.id)
            twt_date = str(tweet.created_at)
            if twt_id not in db_twitter_id:
                if twt_date not in db_twitter_date:
                    #Here is have changed the date unsure if it will effect my dataframe
                    tweet_dates.append(twt_date)
                    tweet_text.append(tweet.full_text)
                    tweet_ids.append(twt_id)


        return tweet_dates, tweet_text, tweet_ids

    def filter_tweets(self, items):
        """Remove all Hast tags, RT and emjois"""
        items = re.sub('http\S+', ' ', items)
        items = re.sub('@\S+', ' ', items)
        items = re.sub('#\S+', ' ', items)
        items = re.sub('\\n', ' ', items)
        items = re.sub(r'RT[\s]+', ' ', items)
        items = re.sub('•\S+', ' ', items)
        items = re.sub('\&amp\S+', ' ', items)
        items = re.sub('\$\S+', ' ', items)
        items = re.sub('\*\S+', ' ', items)
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoj, '', items).strip()

    def getsubjectivity(self, text):
        """Subjectivity quantifies the amount of personal opinion and factual information contained in the text"""
        return textblob.TextBlob(text).sentiment.subjectivity

    def getpolarity(self, text):
        return textblob.TextBlob(text).sentiment.polarity

    def putting_data_df(self, tweet_dates, tweet_text):
        """Sorting out data and putting into pandas"""
        tweet_text = list(map(self.filter_tweets, tweet_text))
        tweet_text = [x.replace('  ', '') for x in tweet_text]
        df = pd.DataFrame({'time_of_tweet': tweet_dates, 'Tweet_text': tweet_text})
        # formatting the time to get rid of local time UDC timing
        df['time_of_tweet'] = pd.to_datetime(df['time_of_tweet']).dt.tz_localize(None)
        # Here we use the twitter text from API and put it into Textblob
        df['subjectivity'] = df['Tweet_text'].apply(self.getsubjectivity)
        df['polairty'] = df['Tweet_text'].apply(self.getpolarity)
        # print(df.head())
        return df

    def polairty_results(self, data):
        """algo to determin results ready for counting"""
        if data < 0:
            return 'Negative'
        elif data == 0:
            return 'Netural'
        else:
            return 'Positive'

    def subjectivity_results(self, data):
        if data < 0.35:
            return 'Factual'
        elif data > 0.35 and data < 0.6:
            return 'Mixed'
        else:
            return 'Opinionated'


    def filter_df_for_db(self, df):
        """taken in df going through results and formatting ready for DB"""
        df['polairty_results'] = df['polairty'].apply(self.polairty_results)
        df['subjectivity_results'] = df['subjectivity'].apply(self.subjectivity_results)
        # print(df.head(10))
        # Putting data into catgoery so they always displayed a fix list amount for DB
        polairty_category = ['Positive', 'Netural', 'Negative']
        subjectivity_category = ['Opinionated', 'Mixed', 'Factual']
        # convert to categorical
        df['polairty_results'] = df['polairty_results'].astype('category')
        df['subjectivity_results'] = df['subjectivity_results'].astype('category')
        # set categories and ordered=True
        df['polairty_results'] = df['polairty_results'].cat.set_categories(polairty_category, ordered=True)
        df['subjectivity_results'] = df['subjectivity_results'].cat.set_categories(subjectivity_category, ordered=True)

        # getting the total for each results
        r1 = df['polairty_results'].value_counts().sort_index(ascending=False)
        r2 = df['subjectivity_results'].value_counts().sort_index(ascending=False)
        r1 = list(r1)
        r2 = list(r2)
        total = r1[0] + r1[1] + r1[2]
        print(f'total tweets {total}')
        print('')
        pol_sub_total_results = r1 + r2
        # print(pol_sub_total_results)

        # Another method of calcuation is merge count
        db_pol_sub = df.groupby('polairty_results')['subjectivity_results'].value_counts().sort_index(ascending=False)
        db_pol_sub = list(db_pol_sub)
        # print(db_pol_sub)

        return pol_sub_total_results, db_pol_sub

    def word_analyse(self, df):

        # Putting each word into a list to be looked at individually
        lines = list()
        for line in df['Tweet_text']:
            words = line.split()
            for w in words:
                lines.append(w)

        # remove all strange characters
        lines = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in lines]
        lines2 = [word for word in lines if word != '']

        # This is stemming the words to their root
        # The Snowball Stemmer requires that you pass a language parameter
        s_stemmer = SnowballStemmer(language='english')
        stem = [s_stemmer.stem(word) for word in lines2]
        # print(stem)

        stem2 = [word for word in stem if word not in nlp.Defaults.stop_words]
        # print(stem2)
        df2 = pd.DataFrame(stem2)
        df2 = df2[0].value_counts()
        df2 = df2[:20,]

        # print(df2)
        # print(type(df2))

        return df2


    def upload_db(self, pol_sub_total_results, db_pol_sub, df2, tweet_dates, tweet_ids):
        """uploading to three different DB"""
        # Needs 6 items in list
        self.insert_total_pol_sub(pol_sub_total_results)
        print(pol_sub_total_results)
        sleep(0.5)
        # Needs 9 items in list
        self.insert_polairty_with_subjectivity_results(db_pol_sub)
        sleep(0.5)
        print(db_pol_sub)
        # needs 2 items in list
        # not saving the words yet
        # self.insert_twitter_key_words(df2)
        # sleep(0.5)
        # print(df2)

        # here is where we add to another table that is the checker

        checker_list = list(zip(tweet_dates, tweet_ids))
        self.insert_twitter_checker_db(checker_list)


    def call_all_twiiter(self):
        self.api_keys()
        db_twitter_date, db_twitter_id = self.get_db_twitter_ids_dates()
        tweet_dates, tweet_text, tweet_ids = self.get_tweets(db_twitter_date, db_twitter_id)
        df = self.putting_data_df(tweet_dates, tweet_text)
        pol_sub_total_results, db_pol_sub = self.filter_df_for_db(df)
        df2 = self.word_analyse(df)
        self.upload_db(pol_sub_total_results, db_pol_sub, df2, tweet_dates, tweet_ids)
        # print(len(pol_sub_total_results, db_pol_sub, df2, tweet_dates, tweet_ids))

#


# test = Get_Twitter_Sentiment('crypto_twitter_sentiment')
# test.call_all_twiiter()
# test.api_keys()
# db_twitter_date, db_twitter_id = test.get_db_twitter_ids_dates()
# tweet_dates, tweet_text, tweet_ids = test.get_tweets(db_twitter_date, db_twitter_id)
# df = test.putting_data_df(tweet_dates, tweet_text)
# pol_sub_total_results, db_pol_sub = test.filter_df_for_db(df)
# df2 = test.word_analyse(df)
# test.upload_db(pol_sub_total_results, db_pol_sub, df2, tweet_dates, tweet_ids)
#
#
# 



