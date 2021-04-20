#   Author: Allen

#  This program accesses data from a twitter user site (hard-coded as Stevens)

#  To run in a terminal window:   python3  best.py


import tweepy
import os

### PUT AUTHENTICATOIN KEYS HERE ###
CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_KEY_SECRET = os.environ.get("TWITTER_CONSUMER_KEY_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

# Authentication

authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#  use wait_on_rate_limit to avoid going over Twitter's rate limits
api = tweepy.API(authenticate, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user_input = ""
while user_input.upper() != "STOP":               
    # Get Information About a Twitter User Account
    user_input = str(input("Please enter the Twitter User Screen Name: "))

    # Stop program if "stop" is entered 
    if user_input.upper() == "STOP": break

    # Get Basic Account Information
    twitter_user = api.get_user(user_input)
    print("Screen Name: ", twitter_user.screen_name)
    print("User name: ", twitter_user.name)
    print("User ID: ", twitter_user.id)
    print("User Description: ", twitter_user.description)
    print("User Location: ", twitter_user.location)
    print("Number of Friends: ", twitter_user.friends_count)
    print("Number of Followers: ", twitter_user.followers_count)

    # Get Last 5 followers from inputed user
    print(" ")
    print("Last 5 followers:")
    twitter_followers = api.followers(user_input)

    for follower in twitter_followers[-5:]:
        print(follower._json['screen_name'])

    # Get Last 5 tweets from inputed user
    print(" ")
    print("Last 5 tweets:")
    twitter_timeline = api.user_timeline(user_input)
    i = 1

    for tweet in twitter_timeline[-5:]:
        print("TWEET " + str(i) + ": " + tweet._json['text'])
        i += 1
        print(" ")


    