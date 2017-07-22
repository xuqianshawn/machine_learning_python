import pandas as pd
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from nltk.stem.lancaster import LancasterStemmer
import re
import msmt
class LinkedIn:
   'Common base class for all employees'
   Count = 0
   st = LancasterStemmer()
   token = msmt.get_access_token('xuqian89', 'qosUksNnkcN17x5Ea/bo5YA1IAdJU81rmEFUi36bBJE=')
   def __init__(self,text):

      self.text = text

      #pureText=BeautifulSoup(self.text).getText().lower()
      pureText=re.sub(r'[?|$|.|!|@|#|-|_|<|>|*|&|[|]|,]',r' ',text)
      pureText = msmt.translate(self.token,pureText,'en')

      pureText=BeautifulSoup(self.text).getText().lower()

      stemmedText=' '.join([self.st.stem(word) for word in pureText.split()])
      removedStoptext = ' '.join([word for word in stemmedText.split() if word not in (stopwords.words('english'))])
      self.meaningfulText=removedStoptext.lower()
      print(self.meaningfulText)
      LinkedIn.Count += 1

#
# def main():
#
#   # Build a service object for interacting with the API. Visit
#   # the Google APIs Console <http://code.google.com/apis/console>
#   # to get an API key for your own application.
#   service = build('translate', 'v2',
#             developerKey='AIzaSyDRRpR3GS1F1_jKNNM9HCNd2wJQyPG3oN0')
#   print(service.translations().list(
#       source='en',
#       target='fr',
#       q=['flower', 'car']
#     ).execute())