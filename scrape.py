from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from time import sleep
import pandas as pd
import numpy as np
import json
import datetime
import settings
import os
import numpy as np
import shutil
import tweepy
import json
import math
import glob
import csv
import zipfile
import zlib
from tweepy import TweepError
from time import sleep

# get twitter handle
#twitterHandle = input('Insert Twitter Handle: ')
dffff = pd.read_csv('info.csv', header = None)

number_of_users = len(dffff.index) - 1
#number_of_users = 3

#print(number_of_users)

current_user = 1

while current_user <= number_of_users:
    twitterHandle = dffff.iloc[current_user, 3]
    print(twitterHandle)
    #current_user += 1

    # edit these three variables
    user = twitterHandle
    start = datetime.datetime(2017, 11, 6)  # year, month, day
    end = datetime.datetime(2018, 11, 6)  # year, month, day
    #start = datetime.datetime(2018, 11, 1)  # year, month, day FOR TESTING
    #end = datetime.datetime(2018, 11, 6)  # year, month, day FOR TESTING

    # only edit these if you're having problems
    delay = 1  # time to wait on each page load before reading the page
    driver = webdriver.Safari()  # options are Chrome() Firefox() Safari()


    # don't mess with this stuff
    twitter_ids_filename = 'all_ids.json'
    days = (end - start).days + 1
    id_selector = '.time a.tweet-timestamp'
    tweet_selector = 'li.js-stream-item'
    user = user.lower()
    ids = []

    def format_day(date):
        day = '0' + str(date.day) if len(str(date.day)) == 1 else str(date.day)
        month = '0' + str(date.month) if len(str(date.month)) == 1 else str(date.month)
        year = str(date.year)
        return '-'.join([year, month, day])

        
    def form_url(since, until):
        p1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A'
        p2 =  user + '%20since%3A' + since + '%20until%3A' + until + 'include%3Aretweets&src=typd'
        p3 = ''
        p4 = ''
        return p1 + p2

    def increment_day(date, i):
        return date + datetime.timedelta(days=i)

    for day in range(days):
        d1 = format_day(increment_day(start, 0))
        d2 = format_day(increment_day(start, 1))
        url = form_url(d1, d2)
        print(url)
        print(d1)
        driver.get(url)
        sleep(delay)

        try:
            found_tweets = driver.find_elements_by_css_selector(tweet_selector)
            increment = 10

            while len(found_tweets) >= increment:
                print('scrolling down to load more tweets')
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(delay)
                found_tweets = driver.find_elements_by_css_selector(tweet_selector)
                increment += 10

            print('{} tweets found, {} total'.format(len(found_tweets), len(ids)))

            for tweet in found_tweets:
                try:
                    id = tweet.find_element_by_css_selector(id_selector).get_attribute('href').split('/')[-1]
                    ids.append(id) 
                except StaleElementReferenceException as e:
                    print('lost element reference', tweet)

        except NoSuchElementException:
            print('no tweets on this day')

        start = increment_day(start, 1)


    try:
        with open(twitter_ids_filename) as f:
            all_ids = ids + json.load(f)
            data_to_write = list(set(all_ids))
            print('tweets found on this scrape: ', len(ids))
            print('total tweet count: ', len(data_to_write))
    except FileNotFoundError:
        with open(twitter_ids_filename, 'w') as f:
            all_ids = ids
            data_to_write = list(set(all_ids))
            print('tweets found on this scrape: ', len(ids))
            print('total tweet count: ', len(data_to_write))

    with open(twitter_ids_filename, 'w') as outfile:
        json.dump(data_to_write, outfile)

    print('all done here')
    driver.close()

    # CHANGE THIS TO THE USER YOU WANT
    user = twitterHandle

    with open('api_keys.json') as f:
        keys = json.load(f)

    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token'], keys['access_token_secret'])
    api = tweepy.API(auth)
    user = user.lower()
    output_file = '{}.json'.format(user)
    output_file_short = '{}_short.json'.format(user)
    compression = zipfile.ZIP_DEFLATED

    with open('all_ids.json') as f:
        ids = json.load(f)

    print('total ids: {}'.format(len(ids)))

    all_data = []
    start = 0
    end = 100
    limit = len(ids)
    i = math.ceil(limit / 100)

    for go in range(i):
        print('currently getting {} - {}'.format(start, end))
        sleep(6)  # needed to prevent hitting API rate limit
        id_batch = ids[start:end]
        start += 100
        end += 100
        tweets = api.statuses_lookup(id_batch)
        for tweet in tweets:
            all_data.append(dict(tweet._json))

    print('metadata collection complete')
    print('creating master json file')
    with open(output_file, 'w') as outfile:
        json.dump(all_data, outfile)

    print('creating ziped master json file')
    zf = zipfile.ZipFile('{}.zip'.format(user), mode='w')
    zf.write(output_file, compress_type=compression)
    zf.close()

    results = []

    def is_retweet(entry):
        return 'retweeted_status' in entry.keys()

    def get_source(entry):
        if '<' in entry["source"]:
            return entry["source"].split('>')[1].split('<')[0]
        else:
            return entry["source"]

    with open(output_file) as json_data:
        data = json.load(json_data)
        for entry in data:
            t = {
                "created_at": entry["created_at"],
                "text": entry["text"],
                "in_reply_to_screen_name": entry["in_reply_to_screen_name"],
                "retweet_count": entry["retweet_count"],
                "favorite_count": entry["favorite_count"],
                "source": get_source(entry),
                "id_str": entry["id_str"],
                "is_retweet": is_retweet(entry)
            }
            results.append(t)

    print('creating minimized json master file')
    with open(output_file_short, 'w') as outfile:
        json.dump(results, outfile)

    with open(output_file_short) as master_file:
        data = json.load(master_file)
        fields = ["favorite_count", "source", "text", "in_reply_to_screen_name", "is_retweet", "created_at", "retweet_count", "id_str"]
        print('creating CSV version of minimized json master file')
        f = csv.writer(open('{}.csv'.format(user), 'w'))
        f.writerow(fields)
        for x in data:
            f.writerow([x["favorite_count"], x["source"], x["text"], x["in_reply_to_screen_name"], x["is_retweet"], x["created_at"], x["retweet_count"], x["id_str"]])

    current_path = os.getcwd()

    #create subdirectory
    move_path = "%s/%s" % (current_path, twitterHandle) #define path
    try:
        os.mkdir(move_path)
    except OSError:
        print ("no no no no nooO")
    else:
        print ("yah yeet")

    #move csv file
    src_csv = "%s/%s.csv" % (current_path, twitterHandle)
    dest_csv = "%s/%s/%s.csv" % (current_path, twitterHandle, twitterHandle)

    try:
        os.rename(src_csv, dest_csv)
    except OSError:
        print ("nah brah")
    else:
        print ("360 no scope")

    #move zip file
    src_zip = "%s/%s.zip" % (current_path, twitterHandle)
    dest_zip = "%s/%s/%s.zip" % (current_path, twitterHandle, twitterHandle)

    try:
        os.rename(src_zip, dest_zip)
    except OSError:
        print ("nah brah")
    else:
        print ("360 no scope")

    #move json file
    src_json = "%s/%s.json" % (current_path, twitterHandle)
    dest_json = "%s/%s/%s.json" % (current_path, twitterHandle, twitterHandle)

    try:
        os.rename(src_json, dest_json)
    except OSError:
        print ("nah brah")
    else:
        print ("360 no scope")

    #move short json file
    src_short = "%s/%s_short.json" % (current_path, twitterHandle)
    dest_short = "%s/%s/%s_short.json" % (current_path, twitterHandle, twitterHandle)

    try:
        os.rename(src_short, dest_short)
    except OSError:
        print ("nah brah")
    else:
        print ("360 no scope")

    #move all_ids.json
    src_all = "%s/all_ids.json" % (current_path)
    dest_all = "%s/%s/all_ids.json" % (current_path, twitterHandle)

    try:
        os.rename(src_all, dest_all)
    except OSError:
        print ("nah brah")
    else:
        print ("360 no scope")

    #df = pd.read_csv('%s/%s/%s.csv' % (current_path, twitterHandle, twitterHandle))

    #get twitterhandle and number of tweets into csv file
    #len(data_to_write

    df = pd.read_csv('twitnum.csv', header = None)

    ddf = pd.DataFrame([[twitterHandle, len(data_to_write)]], columns = list('AB') )

    df = df.append(pd.Series(np.array([0])), ignore_index = True)
    with open('twitnum.csv', 'a') as f:
        ddf.to_csv(f, header = False)
        print('yay')

    current_user += 1

