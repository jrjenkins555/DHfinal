from twarc import Twarc
import tweepy
import pandas as pd
import numpy as np
import csv
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from spacy.lang.en.stop_words import STOP_WORDS
import random

stop = set(STOP_WORDS)

print("making wordclouds")

consumer_key = "SZ524Ewd5YBwo8U0beMBoStzl"
consumer_secret = "ucARFmcMMglJxkUBbVbW9mPjJZd27ZLEPX3OEa2SmhEPGxvhEk"
access_key = "1517196453747298306-9RWrgR5lwbwznq3U53opZaXhEt9ZtH"
access_key_secret = "sTAq6k9GSoKIuDeUBft8lGXwLhIMltvY1O34geSVj1f40"
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHP7bgEAAAAA%2BASXrzsHwu1hjPNtwfzmgwiwsWs%3Dfo4j17ieljbcfordGUBEUwUJzmvbBF1Sk49Nd6IWCa8SvcroEs"
# api = Twarc(consumer_key, consumer_secret, access_key, access_key_secret)

client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_key, access_key_secret)

# March, 2020
lows = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_593.csv", header=None)

# May, 2020
highs = pd.read_csv(filepath_or_buffer="/Users/jrjenkins/Documents/DATA/Spring_2022/ENGL009/Final Project/Datasets/corona_tweets_662.csv", header=None)

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

words_beg = []

while len(words_beg) < 500 :
	sample = lows.sample(n=1)
	sample = sample[0].tolist()[0]
	tweet = client.get_tweet(sample).data
	if tweet :
		tweet = tweet['text']
		words = tweet.split(" ")
		for word in words :
			if not word.isalpha() or (word in stop) or word == 'RT' :
				continue
			words_beg.append(word)

dictBeg = Counter(words_beg)
freqBeg = {k: v/len(dictBeg) for k, v in dictBeg.items()}

wcBeg = WordCloud(background_color="black",width=1000,height=1000, max_words=50,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(freqBeg)
plt.imshow(wcBeg.recolor(color_func=grey_color_func))
plt.savefig('figures/omicron/wcBeg.png')

#############################################

words_end = []

while len(words_end) < 500 :
	sample = highs.sample(n=1)
	sample = sample[0].tolist()[0]
	tweet = client.get_tweet(sample).data
	if tweet :
		tweet = tweet['text']
		words = tweet.split(" ")
		for word in words :
			if not word.isalpha() or (word in stop) or word == 'RT' :
				continue
			words_end.append(word)

dictEnd = Counter(words_end)
freqEnd = {k: v/len(dictEnd) for k, v in dictEnd.items()}

wcEnd = WordCloud(background_color="black",width=1000,height=1000, max_words=50,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(freqEnd)
plt.imshow(wcEnd.recolor(color_func=grey_color_func))
plt.savefig('figures/omicron/wcEnd.png')