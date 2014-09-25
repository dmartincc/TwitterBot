# -*- coding: utf-8 -*-
import time, json, random
import tweepy
import urllib, httplib

CONSUMER_KEY = 'WbrceSUfeRAmZSFS1tYg1Q'
CONSUMER_SECRET = '1YfHQhN0UKOOWADQNlUDDXsW9Qe1AwfwMLoaupc8D5U' # Make sure access level is Read And Write in the Settings tab
ACCESS_KEY = '2195839842-66q0OxCDSDX2btqg69Rt1gKKzK4WOzahIU8jUjo'
ACCESS_SECRET = 'aQhbRKWWENlkxJva3J9YMQ4pogZw5dMWvI4UPhRFyDEAS'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def fetchsamples():
    url = "http://pipes.yahoo.com/pipes/pipe.run?_id=9c8c3a4b218215e6e02182787a522372&_render=json"
    response = urllib.urlopen(url)
    data = response.read()
    jsonData = json.loads(data)    
    news  = jsonData['value']['items']
    phrases =['elobjetivista.com tu portal de titulares aleatorios #noticias',
             'Descubre la nueva forma de leer las #noticias en elobjetivista.com',
             'Lee las #noticias, create una opinión en elobjetivista.com',
             'Todas las #noticias en elobjetivista.com']
                      
    if len(news) != 0:
        int = random.randrange(1,len(news))
        tweet = news[int]['title']  
        text = tweet + " #noticias bit.ly/1fk7HaL"
        if len(text) <= 105:
            post = text
        else:                     
            post = phrases[random.randrange(0,len(phrases)-1)]
    else:
        post = phrases[random.randrange(0,len(phrases)-1)]
    
    trends = api.trends_place('23424950')
    
    i = 0
    size = len(post)
    while size < 130:  
        hashtag = trends[0]['trends'][i+1]['name']
        size = len(post) + len(" "+hashtag) 
        if size < 130:
            post = post +" "+ hashtag
        i += 1     
    
    return post   
    

def postTweet():
    while True:
        text = fetchsamples()
        api.update_status(text)    
        # Random sleep
        snooze = random.randrange(1000,5000)
        time.sleep(snooze)

postTweet()