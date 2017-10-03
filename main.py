import sys
import tweepy
import wolframalpha
import speech_recognition as sr
import re
from pymarkovchain import MarkovChain
from gtts import gTTS
import os

#excluded for public copy
key = " "
secret = " "
token = " "
token_secret = " "
markDirectory = ""

def populateTweets(api, pages, user):
    tweets = []
    
    for i in range (0, pages):
        user_timeline = api.user_timeline(screen_name=user, page = i)
        for status in user_timeline:
            tweets.append(status.text)

    return tweets

def createSuperString(file):
    superString = ""

    infile = open(file, 'r')

    for line in infile:
        superString += line

    superString = re.sub('\n', ' ', superString)
    superString = re.sub('-', ' ', superString)

    return superString

def main():
    auth = tweepy.OAuthHandler(key, secret)
    auth.set_access_token(token, token_secret)
    client = tweepy.API(auth)
    api = tweepy.API(auth)

    tweets = []
    superString = ""
   
    mc = MarkovChain(markDirectory)
    superString = createSuperString('trump.txt')
    mc.generateDatabase(superString)

  
    while(True):
        phrase = mc.generateString()
        try:
            print(phrase)
        except UnicodeEncodeError:
            continue
        try:
            answer = input()
            if(answer == 'y'):
                client.update_status(phrase)
        except tweepy.TweepError:
            continue
    
main()
