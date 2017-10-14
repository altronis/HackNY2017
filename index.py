import tweepy
import os
import json
from rake_nltk import Rake

CONSUMER_KEY = '1nAA0T2RHF7x3v05nHVpbSdCo'
CONSUMER_SECRET = 'Sp46w9cnSRKzYVNoHPTVq1CT4pFpOgUq2h9k0XGslZ5kqBQcaD'
ACCESS_TOKEN = '919279133368123393-Q0s8JYDV8S1J6kW8FWdtfuAlt4TzZTz'
ACCESS_SECRET = 'ibMKNpAW4ZSfAem2V4wM1mj5U783o4hYwfD82rHneiQCN'
oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(oauth)

r = Rake()
for mention in tweepy.Cursor(api.mentions_timeline).items():
    message = ''
    print(mention.text.replace('@FactCheckBotHNY', ''))
    user_tweet_to = '@'+mention.user.screen_name
    message += user_tweet_to
    r.extract_keywords_from_text(mention.text.replace('@FactCheckBotHNY', ''))
    ranked_phrases = r.get_ranked_phrases()
    
    
    #api.update_status(message)
    
    
