import tweepy
import os
from twitter_sentimant.twitter_db import Twitter_Senitment_DB


crypto_name =['MartiniGuyYT', 'MMCrypto', 'Bitboy_Crypto', 'TheCryptoZombie', 'TheMoonCarl']

word_list = ['bitcoin', 'pump', 'pumping', 'dump', 'dumping', 'bull market', 'bear market', 'down' ]

class Case_Study_Twitter(Twitter_Senitment_DB):

    def api_keys(self):
        """Getting my APi keys"""
        path = os.path.abspath(os.path.dirname(__file__))
        print(path)

        with open(path + '\details.txt', 'r') as all_keys:
            # must use this way to get rid of the \n
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

    def get_tweets(self):
        """Search for our key word and send query through to twitter API"""
        #Great for search a cetain person like eleon musk
        # for names in crypto_name:
        tweet_cursor = self.api.user_timeline(screen_name='MartiniGuyYT', count=10, exclude_replies=True, tweet_mode="extended")
        for tweet in tweet_cursor:
            if tweet.full_text in word_list:
                print(tweet.full_text)
            # print(tweet.created_at)
            # print(tweet.id)
            # print(tweet.full_text)
            # print('')



test = Case_Study_Twitter('crypto_twitter_sentiment')
test.api_keys()
test.get_tweets()