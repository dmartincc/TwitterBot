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
    int = random.randrange(1,len(news))
    tweet = news[int]['title']  
    text = tweet + " #noticias elobjetivista.com".encode("utf-8") 
    if len(text) <= 140:
        post = text
    else:
        post = "elobjetivista.com tu portal de titulares aleatorios #noticias"    
    return post   
    #int = random.randrange(1,len(news))
    #tweet = news[int]
    #return tweet 

def postTweet():
    while True:    
        text = fetchsamples()
        api.update_status(text)    
        # Sleep for 1 hour
        time.sleep(300)
        
postTweet()