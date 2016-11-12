# -*- coding: utf-8 -*-
import time, json, random
import tweepy
import urllib, httplib

CONSUMER_KEY = 'AeOqFHSyQNnWmap7X8mFtG8Jx'
CONSUMER_SECRET = '3MKUBScQzoODUupqNOVZfHFXE6vO5pEg9C6pOMhbs6YiZvNlqn'
ACCESS_KEY = '790273061014691840-dz26yzvaIQommWx0Bnot3UhcBRHFjjc'
ACCESS_SECRET = '0sEvAq3Xk6zmBEEIeFylClKZLC8W9p94bEMvvEDwU3fxE'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def get_news():
    keywords = ['air pollution','air quality', 'calidad aire', 'contaminación aire']
    int_ = random.randrange(0, len(keywords)-1)
    url = "https://kenkobot.me/api/v1/news?keywords={}".format(keywords[int_])
    response = urllib.urlopen(url)
    data = response.read()
    jsonData = json.loads(data)    
    news  = jsonData['result']
    phrases =[
        'Do you know the air quality you are breathing? Join me and I will inform you https://kenkobot.me/?ref=twitter',
        'Reduce your carbon footprint by using public transport and be aware of the air quality around you https://kenkobot.me/?ref=twitter',
        'Keep your children save by knowing the air they are breathing https://kenkobot.me/?ref=twitter',
        'Do you exercise outdoors? Know the air you breath https://kenkobot.me/?ref=twitter',
        'Did you know that every 5 seconds a person dies due to air pollution https://kenkobot.me/?ref=twitter',
        'Air pollution, a real hazard in cities https://kenkobot.me/?ref=twitter',
    ]
                      
    if len(news) != 0:
        int = random.randrange(1,len(news))
        tweet = news[int]['title'] + news[int]['link']
        text = tweet.encode("utf8")
        if len(text) < 150:
            post = text
        else:                     
            post = phrases[random.randrange(0,len(phrases)-1)].encode("utf8")
    else:
        post = phrases[random.randrange(0,len(phrases)-1)].encode("utf8")

    return post

def get_station_aqi():
    url = "https://kenkobot.me/api/v1/station-aqi/"
    response = urllib.urlopen(url)
    data = response.read()
    jsonData = json.loads(data)    
    data  = jsonData['result']
    rand = random.random()
    if rand < 0.5:
        msg = {
            'msg' :"Now at {} the air quality is {}, dominant pollutant {}. AQI {} https://kenkobot.me?ref=twitter".format(
                data['station'],
                data['now']['type'],
                data['pollutant'],
                data['now']['index']
            ),
            'img': data['now']['img']
        }
    else:
        msg = {
            'msg' : "Tomorrow at {} the air quality will be {}, AQI {} https://kenkobot.me?ref=twitter".format(
                data['station'],
                data['forecast']['type'],
                data['forecast']['index']
            ),
            'img': data['forecast']['img']
        }

    return msg
  
def get_trends(post):
    trends = api.trends_place('1')
    i = 0
    size = len(post)
    while size < 130:  
        hashtag = trends[0]['trends'][i+1]['name']
        size = len(post) + len(" "+hashtag) 
        if size < 130:
            post = post +" "+ hashtag
        i += 1     
    
    return post

def compose_status():
    rand = random.random()
    if rand > 0.9:
        msg = get_news()
        # msg = get_trends(msg)
        api.update_status(msg)  
    else:
        msg = get_station_aqi()
        # msg['msg'] = get_trends(msg['msg'])
        if len(msg['msg']) < 130:
            f = open('image.jpg','wb')
            f.write(urllib.urlopen(msg['img']).read())
            f.close()
            api.update_with_media('image.jpg', status=msg['msg'])
    print msg
        
   
def postTweet():
    while True:
        try:
            compose_status() 
        except:
            pass
        # Random sleep
        snooze = random.randrange(1,5)
        time.sleep(snooze)

postTweet()