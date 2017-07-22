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
class Train:
    linkins=[]
        interests=[]
            def __init__(self):
                print("in init")
                    
                    def getFeature(self):


vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 20)
    #print(self.tweets)
    print('--start--')
    print(len(self.linkins))
    train_data_features = vectorizer.fit_transform(self.linkins)
    train_data_features = train_data_features.toarray()
    print('--feature length--'+str(len(train_data_features)))
    with open("test.txt", "w") as text_file:
        for i in range(0, len(train_data_features)):
            #text_file.write(str(train_data_features[0]).replace('[', '').replace(']', '')+'\n')
            if (i==(len(train_data_features)-1)):
                text_file.write(self.learnString(str(train_data_features[i])))
                    else:
                        text_file.write(self.learnString(str(train_data_features[i]))+'\r\n')
                    print(train_data_features)
return (train_data_features)
    
    
    def learnString(self,str):
        cleanedStr=str
            cleanedStr=cleanedStr.replace('[ ','[').replace('[','').replace('  ',' ').replace(' ',',').replace('\r\n','').replace('\n','').replace(']','')
                return cleanedStr
                    def populateLinkedInText(self,folderName):
counter=0
    for (dirpath, dirnames, filenames) in walk(folderName):
        counter=len(filenames)
        print('total number'+str(counter))
        for i in range(0, counter):
            #get the tweet if, load tweet from json
            if(filenames[i]=='.DS_Store' or filenames[i]=='U100gnd.txt'):
                continue
            with open(folderName+'/'+str(filenames[i])) as data_file:
                data = data_file.read()
                    
                    print(data)
                        #add tweet
                        #print(row[1])
                        linkedin=LinkedIn(data)
                            self.linkins.append(linkedin.meaningfulText)

print(all)
    def populateInterests(self,path):
    with open(path) as data_file:
        data = data_file.read()
            lines = data.split('\n')
                print(lines)
                    for i in range(0, len(lines)):
                        train.interests.append(lines[i])
                            print(train.interests)




train= Train()
train.populateLinkedInText('/Users/xuqianshawn/PycharmProjects/untitled/CS4242Plus/test/LinkedIn')
feature=train.getFeature()
forest = RandomForestClassifier( n_estimators = 100 )
train.populateInterests('/Users/xuqianshawn/PycharmProjects/untitled/CS4242Plus/test/groundTruth.txt')
forest = forest.fit(feature, train.interests)
# s
feature2=train.getFeature()
result = forest.predict(feature2)

# Write the test results
#output = pd.DataFrame( data={"sentiment":result} )
#output.to_csv( "Word2Vec_AverageVectors.csv", index=False, quoting=3 )
#nltk.download()