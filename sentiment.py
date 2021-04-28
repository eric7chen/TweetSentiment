import nltk
from nltk.corpus import stopwords
from nltk.corpus import twitter_samples
from nltk.tokenize import TweetTokenizer
import csv
import os
import shutil
import string
import os.path
from nltk.tokenize import word_tokenize
import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from random import shuffle
import string
import re
from nltk import classify
from nltk import NaiveBayesClassifier
import numpy as np
import time

start = time.time()

info_csv = pd.read_csv('info.csv', header = None)
current_path = os.getcwd()


#print(twitterHandle)

pos_tweets = twitter_samples.strings('positive_tweets.json')
neg_tweets = twitter_samples.strings('negative_tweets.json')
all_tweets = twitter_samples.strings('tweets.20150430-223406.json')
tweet_tokenizer = TweetTokenizer(preserve_case = False, 
										 strip_handles = True, 
										 reduce_len = True)

#current_path = os.path.join('kayiveyforgov')

#print(current_path)

#tweet_csv = pd.read_csv('kayiveyforgov.csv', header = None)

from nltk.corpus import stopwords
stopwords_english = stopwords.words('english')

from nltk.stem import PorterStemmer
stemmer = PorterStemmer()

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)
 
def clean_tweets(tweet):
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
 
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    
    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
 
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
 
    tweets_clean = []    
    for word in tweet_tokens:
        if (word not in stopwords_english and # remove stopwords
              word not in emoticons and # remove emoticons
                word not in string.punctuation): # remove punctuation
            #tweets_clean.append(word)
            stem_word = stemmer.stem(word) # stemming word
            tweets_clean.append(stem_word)
 
    return tweets_clean

def bag_of_words(tweet):
	words = clean_tweets(tweet)
	words_dictionary = dict([word, True] for word in words)
	return words_dictionary

pos_tweets_set = [] #Training
for tweet in pos_tweets:
	pos_tweets_set.append((bag_of_words(tweet), 'pos'))

neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))

#print (len(pos_tweets_set), len(neg_tweets_set))

shuffle(pos_tweets_set)
shuffle(neg_tweets_set)
 
test_set = pos_tweets_set[:1000] + neg_tweets_set[:1000]
train_set = pos_tweets_set[1000:] + neg_tweets_set[1000:]
 
#print(len(test_set),  len(train_set))

classifier = NaiveBayesClassifier.train(train_set)
 
accuracy = classify.accuracy(classifier, test_set)
#print(accuracy) # Output: 0.765
 
#print (classifier.show_most_informative_features(10))

dffff = pd.read_csv('info.csv', header = None)

number_of_users = len(dffff.index) - 1
current_user = 1

while current_user <= number_of_users:
	twitterHandle = info_csv.iloc[current_user, 3]
	current_path = os.path.join('%s' % (twitterHandle))
	tweet_csv = pd.read_csv('%s/%s.csv' % (current_path, twitterHandle), header = None)

	number_of_tweets = len(tweet_csv.index)
	print(number_of_tweets)

	current_tweet = 1
	while current_tweet <= number_of_tweets - 1:
		text = tweet_csv.iloc[current_tweet, 2]
		
		text_set = bag_of_words(text)
		sentiment = classifier.classify(text_set)
		#print(sentiment)

		prob_result = classifier.prob_classify(text_set)
		#print (prob_result)
		#print (prob_result.max())
		#print (prob_result.prob("neg"))
		#print (prob_result.prob("pos"))
		#print(text)
		df = pd.read_csv('twitsent.csv', header = 0)
		ddf = pd.DataFrame([[twitterHandle, sentiment]], columns = list('AB') )
		df = df.append(pd.Series(np.array([0])), ignore_index = True)
		with open('twitsent.csv', 'a') as f:
			ddf.to_csv(f, header = 0)
			#print('yay')

		text_set.clear()

		current_tweet += 1

	current_user += 1

end = time.time()
print(end-start)










