from bs4 import BeautifulSoup
import urllib2
from os import walk
mypath="/Users/xuqianshawn/PycharmProjects/CS4242Plus/Test/LinkedIn/"
txtFeature=""
counter=0
for (dirpath, dirnames, filenames) in walk(mypath):
    counter=len(filenames)
    print('total number'+str(counter))
    for i in range(0, counter):
        if ".html" not in filenames[i]:
         continue
        page = urllib2.urlopen("file://"+mypath+str(filenames[i]))
        print('current parsing'+str(filenames[i]))
        soup = BeautifulSoup(page)
        try:
            CurrentIndustry=soup.find("dd",class_="industry").find('a').text
            print(CurrentIndustry)
            txtFeature=CurrentIndustry+" "
        except:
         print('cannout find Current Industry')
        try:
         pastJobs=soup.find("tr",id="overview-summary-past").find_all('a',attrs={'dir':'auto'})
         for eachjob in pastJobs:
          print(eachjob.text)
          txtFeature+=eachjob.text++" "
        except:
         print('cannout find post jobs')
        #overview-summary-past
        try:
         description=soup.find("p",class_="description").text
         print(description)
         txtFeature+=description+" "
        except:
         print('cannout find description')
        try:
         endorsedskills=soup.find_all('a',attrs={'class':'endorse-item-name-text'})
         for eachskill in endorsedskills:
          print(eachskill.text)
          txtFeature+=eachskill.text+" "
        except:
          print('cannout find endorsedskill')



        txtFileName=filenames[i].split('.')[0]+".txt"
        file=open(txtFileName, 'w')
        file.write(txtFeature.encode('utf8'))
        file.close()
        i=i+1
