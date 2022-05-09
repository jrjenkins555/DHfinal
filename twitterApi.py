from twarc import Twarc
import tweepy
import pandas as pd
import numpy as np
import csv

print("accessing twitter api...")

consumer_key = "SZ524Ewd5YBwo8U0beMBoStzl"
consumer_secret = "ucARFmcMMglJxkUBbVbW9mPjJZd27ZLEPX3OEa2SmhEPGxvhEk"
access_key = "1517196453747298306-9RWrgR5lwbwznq3U53opZaXhEt9ZtH"
access_key_secret = "sTAq6k9GSoKIuDeUBft8lGXwLhIMltvY1O34geSVj1f40"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHP7bgEAAAAA%2BASXrzsHwu1hjPNtwfzmgwiwsWs%3Dfo4j17ieljbcfordGUBEUwUJzmvbBF1Sk49Nd6IWCa8SvcroEs"
# api = Twarc(consumer_key, consumer_secret, access_key, access_key_secret)

client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_key, access_key_secret)

# March, 2020
lows = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_298.csv", header=None)
lows = lows.sample(n=15)
lows = lows[0].tolist()

# May, 2020
highs = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_313.csv", header=None)
highs = highs.sample(n=15)
highs = highs[0].tolist()

# print(highs)
# tw = client.get_tweet(lows[0]).data
# print(tw)

tweets_mar20 = [client.get_tweet(lows[i]).data for i in range(len(lows))]
tweets_may20 = [client.get_tweet(highs[i]).data for i in range(len(highs))]

np.savetxt("janBeg21.csv", tweets_mar20, delimiter =", ", fmt ='% s')
np.savetxt("janEnd21.csv", tweets_may20, delimiter =", ", fmt ='% s')

