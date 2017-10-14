import tweepy
import os

CONSUMER_KEY = '1nAA0T2RHF7x3v05nHVpbSdCo'
CONSUMER_SECRET = 'Sp46w9cnSRKzYVNoHPTVq1CT4pFpOgUq2h9k0XGslZ5kqBQcaD'
ACCESS_TOKEN = '919279133368123393-Q0s8JYDV8S1J6kW8FWdtfuAlt4TzZTz'
ACCESS_SECRET = 'ibMKNpAW4ZSfAem2V4wM1mj5U783o4hYwfD82rHneiQCN'
oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(oauth)


mentions = api.mentions_timeline(count=1)
for mention in mentions:
    print(mention)

