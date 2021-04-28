import os
import shutil
import pandas as pd
import numpy as np
from get_metadata import *

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















































