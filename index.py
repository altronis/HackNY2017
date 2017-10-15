import tweepy
import os
import time
import sys
import json
import requests
from rake_nltk import Rake
from Naked.toolshed.shell import execute_js, muterun_js
from nytimesarticle import articleAPI
from difflib import SequenceMatcher

def nyt_url_format(s):
    str_list = s.split(' ')
    newstr = str_list[0]
    for i in range(1, len(str_list)):
        newstr += '+' + str_list[i]
    return newstr

def title_compare(s, s2):
    s = s.lower()
    s2 = s2.lower()
    m = SequenceMatcher(None, s, s2)
    return m.ratio()

#GOOGLE
def goo_shorten_url(url):
    post_url = 'https://www.googleapis.com/urlshortener/v1/url?key=AIzaSyB1UayMZUaCYwMTARpYhlKXtgWIP6xxTcg'
    payload = {'longUrl': url}
    headers = {'content-type': 'application/json'}
    r = requests.post(post_url, data=json.dumps(payload), headers=headers)
    data = r.json()
    return data['id']

#PROPUBLICA
def propublica_search(s):
    propub_key = 'hYaO90rhiuKBkcj2gRZ3TGj7Js8byQ55AamkqdPh'
    get_url = 'https://api.propublica.org/congress/v1/bills/search.json?query=' + nyt_url_format(s)
    headers = {'X-API-Key': propub_key}
    r = requests.get(get_url, headers=headers)
    data = r.json()
    print(data)
    return data
    

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

# r = Rake()
for mention in tweepy.Cursor(api.mentions_timeline).items():
    message = ''
    s = mention.text.replace('@FactCheckBotHNY', '')
    user_tweet_to = '@'+mention.user.screen_name
    reply_id = mention.id
    message += user_tweet_to
    # r.extract_keywords_from_text(mention.text.replace('@FactCheckBotHNY', ''))
    # ranked_phrases = r.get_ranked_phrases()

    # print(ranked_phrases)
    urls_to = []
    r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q="+nyt_url_format(s)+"&api-key=223293e7d64544aa8e7eef843508be06")
    data = r.json()
    try:
        nyturl = data["response"]["docs"][0]['web_url']
        urls_to.append(nyturl)
        nyttitle = data["response"]["docs"][0]['snippet']
        ppdata = propublica_search(s)
        ppurl = ppdata["results"][0]["bills"][0]["govtrack_url"]
        urls_to.append(ppurl)
        pptitle = ppdata["results"][0]["bills"][0]["title"]
        print(pptitle)

    ##    print(title_compare(nyttitle, s))
    ##    print(title_compare(pptitle, s))
        avg = (title_compare(nyttitle, s)+title_compare(pptitle, s))/2;
        print(avg)
        if avg >= 0.3:
            message += " My sources lean 'YES': "
        else:
            message += " My sources lean 'NO': "
        time.sleep(1)
    ##    for i in range(0, len(ranked_phrases)):
    ##        print(ranked_phrases[i])
    ##        r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q="+nyt_url_format(ranked_phrases[i])+"&api-key=223293e7d64544aa8e7eef843508be06")
    ##        data = r.json()
    ##        urls_to.append(data["response"]["docs"][0]['web_url'])
    ##        if i == 0:
    ##            print(title_compare(data["response"]["docs"][0]['headline']['main'], ' '.join(ranked_phrases)))
    ##            if title_compare(data["response"]["docs"][0]['headline']['main'], ' '.join(ranked_phrases)) >= 0.3:
    ##                message += " My sources lean 'YES': "
    ##            else:
    ##                message += " My sources lean 'NO': "
    ##        time.sleep(1)
    ##        break
        for url in urls_to:
            message += goo_shorten_url(url) + ' '

        print(message)
        if len(message) > 140:
            message = message[:140]

        api.update_status(message, reply_id)
    except:
        api.update_status(message+' oh no', reply_id)    
    break

    
    
