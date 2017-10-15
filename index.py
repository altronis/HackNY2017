import tweepy
import time
import urllib
import json
import requests
##from Naked.toolshed.shell import execute_js, muterun_js
##from nytimesarticle import articleAPI
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


#GIPHY
def giphy_rand():
    file = open(urllib.request.urlopen(gifurl))
    print(file)
    return file


#beautiful
def shit():
    gif_get_url = "https://api.giphy.com/v1/gifs/random?api_key=mbafGO3L2IFZU2sU6iNlUXYyVyBY2Ob8&tag=funny&rating=PG-13"
    giphy_key = 'mbafGO3L2IFZU2sU6iNlUXYyVyBY2Ob8'
    data = requests.get(gif_get_url).json()
    gifurl = data["data"]["url"]       
    api.update_status(user_tweet_to+' Your tweet makes no sense '+gifurl, reply_id)
                    
                                    
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


for mention in tweepy.Cursor(api.mentions_timeline).items():
    message = ''
    s = mention.text.replace('@FactCheckBotHNY', '')
    user_tweet_to = '@'+mention.user.screen_name
    reply_id = mention.id
    message += user_tweet_to
    urls_to = []
    r = requests.get("http://api.nytimes.com/svc/search/v2/articlesearch.json?q="+nyt_url_format(s)+"&api-key=223293e7d64544aa8e7eef843508be06")
    data = r.json()
    if data["response"]["meta"]["hits"] != 0:
        avg = 0
        for i in range(5):
            avg += title_compare(data["response"]["docs"][i]['headline']['main'], s)
        avg /= 5
        nyturl = data["response"]["docs"][0]['web_url']
        nyttitle = data["response"]["docs"][0]['headline']['main']
        if title_compare(nyttitle, s) >= .20:
            urls_to.append(nyturl)
        print(avg)
        avg = (avg*100-15) * 5
        print(avg)
        message += " I am "+str(int(avg))+"% certain: "
        time.sleep(1)
        for url in urls_to:
            message += goo_shorten_url(url) + ' '
        if len(message) > 140:
            message = message[:140]
        if len(urls_to) == 0:
            shit()
        else:
            print(message)
            api.update_status(message, reply_id)
    else:
        gif_get_url = "https://api.giphy.com/v1/gifs/random?api_key=mbafGO3L2IFZU2sU6iNlUXYyVyBY2Ob8&tag=funny&rating=PG-13"
        giphy_key = 'mbafGO3L2IFZU2sU6iNlUXYyVyBY2Ob8'
        data = requests.get(gif_get_url).json()
        gifurl = data["data"]["url"]       
        api.update_status(message+' Your tweet makes no sense '+gifurl, reply_id)
    break
