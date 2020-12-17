"""
Get Tweets
this contains a python class called apiWrapper
This class is the wrapper for twitter streaming api
it uses tweepy python package.
currently available actions are:
    - authentication
    - collecting covid tweets with requested language and other options
    - getting the persian tweets based on the ids


this package is designed to collect and save the data on files in Data directory
for using the output of this class you can use the created files
"""

__author__ = "Matin Ebrahimkhani"
__copyright__ = "Copyright 2020, twitter analysis for covid tweets with nltk project"
__credits__ = ["Matin Ebrahimkhani", "Arushi Chawla", "Gabriel Preda"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Matin Ebrahimkhani"
__studentID__: str = "994121"

import tweepy as tw
import pandas as pd
from tqdm import tqdm


class apiWrapper:
    def __init__(self):
        self.consumer_api_key = 'XXXXXXXXXXXXXXXXXXXXXX'  # generated from develpers.twitter.com
        self.consumer_api_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'  # generated from develpers.twitter.com

    def authenticate(self):
        self.auth = tw.OAuthHandler(self.consumer_api_key, self.consumer_api_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    def collect_covid_tweets(self, count, file, lang='en', date_since="2020-03-01"):
        search_words = "#covid19 -filter:retweets"
        date_since = date_since
        # Collect tweets
        tweets = tw.Cursor(self.api.search,
                           q=search_words,
                           lang=lang,
                           since=date_since).items(count)
        tweets_copy = []
        for tweet in tqdm(tweets):
            tweets_copy.append(tweet)
        print(f"new tweets retrieved: {len(tweets_copy)}")
        tweets_df = pd.DataFrame()
        for tweet in tqdm(tweets_copy):
            hashtags = []
            try:
                for hashtag in tweet.entities["hashtags"]:
                    hashtags.append(hashtag["text"])
                text = self.api.get_status(id=tweet.id, tweet_mode='extended').full_text
            except:
                pass
            tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name,
                                                       'user_location': tweet.user.location,
                                                       'user_description': tweet.user.description,
                                                       'user_created': tweet.user.created_at,
                                                       'user_followers': tweet.user.followers_count,
                                                       'user_friends': tweet.user.friends_count,
                                                       'user_favourites': tweet.user.favourites_count,
                                                       'user_verified': tweet.user.verified,
                                                       'date': tweet.created_at,
                                                       'text': text,
                                                       'hashtags': [hashtags if hashtags else None],
                                                       'source': tweet.source,
                                                       'is_retweet': tweet.retweeted}, index=[0]))
        tweets_old_df = pd.read_csv(file)
        print(f"past tweets: {tweets_old_df.shape}")
        tweets_all_df = pd.concat([tweets_old_df, tweets_df], axis=0)
        print(
            f"new tweets: {tweets_df.shape[0]} past tweets: {tweets_old_df.shape[0]} all tweets: {tweets_all_df.shape[0]}")
        tweets_all_df.drop_duplicates(subset=["user_name", "date", "text"], inplace=True)
        print(f"all tweets: {tweets_all_df.shape}")
        tweets_df.to_csv(file, index=False)
        print("Done")

    def get_persian_ids(self, outputfile):

        df = pd.DataFrame(columns=['text'])
        # url='https://iasbs.ac.ir/~hkhojasteh/PICS99A4/tweet_ids_v2.0.txt'
        with open('Data/tweet_ids_v2.0.txt') as f:
            ids = f.read().splitlines()
        # print(ids[0:10])
        total = len(ids)
        index = 0
        success = 0
        failed = 0
        df = pd.DataFrame()
        for tweet_id in ids:
            print(f'tweet_id[{index}]:', end=' ')
            index += 1
            try:
                tweet = self.api.get_status(int(tweet_id), tweet_mode='extended')
                hashtags = []
                for hashtag in tweet.entities["hashtags"]:
                    hashtags.append(hashtag["text"])
                df = df.append(pd.DataFrame({'user_name': tweet.user.name,
                                             'user_location': tweet.user.location,
                                             'user_description': tweet.user.description,
                                             'user_created': tweet.user.created_at,
                                             'user_followers': tweet.user.followers_count,
                                             'user_friends': tweet.user.friends_count,
                                             'user_favourites': tweet.user.favourites_count,
                                             'user_verified': tweet.user.verified,
                                             'date': tweet.created_at,
                                             'text': tweet.full_text,
                                             'hashtags': [hashtags if hashtags else None],
                                             'source': tweet.source,
                                             'is_retweet': tweet.retweeted}, index=[0]))
                df.to_csv(outputfile)
                success += 1
                print('Success')
            except:
                failed += 1
                print('Failed')
                pass
        # df.to_csv('covid19_tweets_persian.csv')
        print(f"{total} ids requested - {success} succeeded - {failed} failed")
        print(f"so %{(failed / index) * 100} of ids practically are useless")


if __name__ == '__main__':
    print('starting. . . ')
    twitter_api = apiWrapper()
    twitter_api.authenticate()

    # uncomment code below to get data from api
    twitter_api.get_persian_ids(outputfile='Data/covid19_tweets_persian_withid.csv')
    # twitter_api.collect_covid_tweets(count=5000000, lang='fa', file="covid19_tweets_persian.csv")
    # twitter_api.collect_covid_tweets(count=500, lang='en', file="covid19_tweets.csv")
