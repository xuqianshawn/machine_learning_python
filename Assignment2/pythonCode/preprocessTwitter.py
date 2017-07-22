import pandas as pd
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import CountVectorizer
import csv
import json
from sklearn.ensemble import RandomForestClassifier
from LinkedIn import LinkedIn
from os import walk
import numpy
from nltk.stem.lancaster import LancasterStemmer

# converts the json file into more readable format
def format_json():
	with open('Twitter_U1_1.json') as f:
		with open('Twitter_U1_1_formatted.json', 'wb+') as fw:
			fw.write(f.read().replace(',',',\n'))

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def json2array(file_name):
    data_arr = []
    try:
        with open(file_name, 'r') as f:
    		content = f.read()
        if content != '' and content != None:
            data_arr = json_loads_byteified(content)
    except IOError:
        print "File: " + file_name + " not found"
    print "   length of tweets: " + str(len(data_arr))
    return data_arr

def extract_useful_info(arr):
	useful_arr = ""
	useful_arr+= arr[0]['user']['description']

	for item in arr:
		useful_arr+=(str(item['text']))
		useful_arr+= str([ht['text'] for ht in item['entities']['hashtags']])

	return useful_arr

def getFeature(tweets):


    vectorizer = CountVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = 100)
    #print(self.tweets)
    print('--start--')
    print(len(tweets))
    train_data_features = vectorizer.fit_transform(tweets)
    train_data_features = train_data_features.toarray()
    print('--feature length--'+str(len(train_data_features)))
    with open("testtwitter.txt", "w") as text_file:
     for i in range(0, len(train_data_features)):
      #text_file.write(str(train_data_features[0]).replace('[', '').replace(']', '')+'\n')
      if (i==(len(train_data_features)-1)):
       text_file.write(Format(str(train_data_features[i])))
      else:
       text_file.write(Format(str(train_data_features[i]))+'\r\n')
    print(train_data_features)
    return (train_data_features)
def learnString(str):
       cleanedStr=str
       st=LancasterStemmer()
       pureText=BeautifulSoup(str).get_text().lower()
       removedStoptext = ' '.join([word for word in pureText.split() if word not in (stopwords.words('english'))])
       stemmedText=' '.join([st.stem(word) for word in removedStoptext.split()])
       cleanedStr=re.sub(r'[?|$|.|!|@|#|-|_|<|>|*|&|[|]|,]',r' ',stemmedText)
       cleanedStr.replace('     ',' ').replace('    ',' ').replace('   ',' ').replace('  ',' ')
       print(cleanedStr)
       return cleanedStr
def Format(str):
    cleanedStr=str.replace('[  ','[').replace('[ ','[').replace('[','').replace('  ',' ').replace(' ',',').replace('\r\n','').replace('\n','').replace(']','').replace(',,,',',').replace(',,',',')
    return cleanedStr
trainN = 420
testN = 150
results = []
#convert twitter data to vector
# for i in range(1, trainN+1):
#     print "===user " + str(i) + "==="
#     tweets_arr = []
#     for j in range(1, 4):
#         result = json2array('./CS4242Plus/Train/Twitter/U'+str(i)+'/'+str(j)+'.json')
#         tweets_arr += result
#     results.append(learnString(extract_useful_info(tweets_arr)) if len(tweets_arr)>0 else "")

for i in range(trainN+1, trainN+testN+1):
    print "===user " + str(i) + "==="
    tweets_arr = []
    for j in range(1, 4):
        print(str(i))
        result = json2array('./CS4242Plus/Test/Twitter/U'+str(i)+'/'+str(j)+'.json')
        tweets_arr += result

    results.append(learnString(extract_useful_info(tweets_arr)) if len(tweets_arr)>0 else "")


print len(results)
getFeature(results)

# with open('tweets_formatted.json', 'wb+') as f2:
#     f2.write(json.dumps(results))