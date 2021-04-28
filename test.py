import pandas as pd
import os
import numpy as np
'''#----------------CSV FILES twtinum.csv--------------
current_path = os.getcwd()
twitterHandle = 'sensadersasd'
numTweets = 1123

#df = pd.read_csv('%s/sensanders/sensanders.csv' % current_path)
#print(df)

#new_df = df.drop(['source', 'favorite_count', 'in_reply_to_screen_name', 'created_at', 'retweet_count', 'id_str', 'is_retweet'], axis = 1)
#print(new_df)
df = pd.read_csv('twitnum.csv', header = None)

ddf = pd.DataFrame([[twitterHandle, numTweets]], columns = list('AB') )


df = df.append(pd.Series(np.array([0])), ignore_index = True)
with open('twitnum.csv', 'a') as f:
	ddf.to_csv(f, header = False)



dddf = pd.read_csv('twitnum.csv')

print(dddf)
'''
'''
df = pd.read_csv('info.csv', header = None)

number_of_users = len(df.index) - 1

#print(number_of_users)

current_user = 1

while current_user <= number_of_users:
	twitterHandle = df.iloc[current_user, 3]
	print(twitterHandle)
	current_user += 1
'''

dffff = pd.read_csv('info.csv', header = None)

#number_of_users = len(dffff.index) - 1
number_of_users = 3

#print(number_of_users)

current_user = 1

#while current_user <= number_of_users:
twitterHandle = dffff.iloc[10, 3]
print(twitterHandle)