import tweepy
import os
import time
import sys
import json
import requests
from rake_nltk import Rake
from Naked.toolshed.shell import execute_js, muterun_js
from nytimesarticle import articleAPI

def nyt_url_format(s):
    str_list = s.split(' ')
    newstr = str_list[0]
    for i in range(1, len(str_list)):
        newstr += '+' + str_list[i]
    return newstr

#GOOGLE
def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyB1UayMZUaCYwMTARpYhlKXtgWIP6xxTcg'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    data = r.json()
    return data['id']

#TWITTER
CONSUMER_KEY = '1nAA0T2RHF7x3v05nHVpbSdCo'
CONSUMER_SECRET = 'Sp46w9cnSRKzYVNoHPTVq1CT4pFpOgUq2h9k0XGslZ5kqBQcaD'
ACCESS_TOKEN = '919279133368123393-Q0s8JYDV8S1J6kW8FWdtfuAlt4TzZTz'
ACCESS_SECRET = 'ibMKNpAW4ZSfAem2V4wM1mj5U783o4hYwfD82rHneiQCN'
oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(oauth)

#NYTIMES
NYT_api_key = '223293e7d64544aa8e7eef843508be06'


JS_TO_RUN = 'index.js'

r = Rake()
for mention in tweepy.Cursor(api.mentions_timeline).items():
    message = ''
    print(mention.text.replace('@FactCheckBotHNY', ''))
    user_tweet_to = '@'+mention.user.screen_name + ' '
    reply_id = mention.id
    message += user_tweet_to
    r.extract_keywords_from_text(mention.text.replace('@FactCheckBotHNY', ''))
    ranked_phrases = r.get_ranked_phrases()

    print(ranked_phrases)
    urls_to = []
    for rp in ranked_phrases:
        print(rp)
        r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q="+nyt_url_format(rp)+"&api-key=223293e7d64544aa8e7eef843508be06")
        data = r.json()
        urls_to.append(data["response"]["docs"][0]['web_url'])
        time.sleep(1)
    for url in urls_to:
        message += goo_shorten_url(url) + ' '

    print(message)
    api.update_status(message, reply_id)
    break

    #api.update_status(message)
    
    
