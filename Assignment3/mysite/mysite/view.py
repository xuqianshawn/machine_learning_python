from django.http import HttpResponse
from django.shortcuts import render
from .RBuddy import RBuddy
from .models import Runner
from django.core import serializers
import json
def index(request):
    return render(request, 'Runner.html')

# def LoadSingleRunners(request, runnerid):
#     if(len(runnerid)<5):
#      return HttpResponse('test')
#     else:
#      returnlist=request.session['runnerlist']
#      for runner in returnlist:
#          if(runner.user_id==runnerid):
#           return runner.to_JSON()
#      return HttpResponse('test')
def LoadRunners(request, runnerid):
    if(len(runnerid)<5):
      return HttpResponse(runnerid);
    file_path = "./mysite/runners.json"
    rbuddy = RBuddy()
    rbuddy.load_buddies(file_path)
    for id in rbuddy.profiles:
     print(id)
     if(id!=runnerid):

        continue
     else:
       newlist=(rbuddy.recommend_buddies(rbuddy.profiles[id], 10))
    # #print (list)
    #
    # print(rbuddy.get_profile(list[0]).averageDistance)
    # print(rbuddy.get_profile(list[0]).averageSinuosity)
    # print(rbuddy.get_profile(list[0]).type)
    runnerlist=[]

    #add myself to the first of list
    temp=(rbuddy.get_profile(runnerid))
    runner= Runner()
    runner.name=temp.user_id
    runner.gender=temp.gender
    runner.weight=temp.weight
    runner.height=temp.height
    runner.type=temp.type
    runner.averageSpeed=temp.averageSpeed
    runner.averageDistance=temp.averageDistance
    runner.averageDuration=temp.averageDuration
    runner.averageSinuosity=temp.averageSinuosity
    runner.lat=str(temp.averageCenterpoint).split(',')[0].replace('(','').replace(' ','')
    runner.lon=str(temp.averageCenterpoint).split(',')[1].replace(')','').replace(' ','')
    runnerlist.append(runner)

    for rid in newlist:
        temp=(rbuddy.get_profile(rid))
        runner= Runner()
        runner.name=temp.user_id
        runner.gender=temp.gender
        runner.weight=temp.weight
        runner.height=temp.height
        runner.type=temp.type
        runner.averageSpeed=temp.averageSpeed
        runner.averageDistance=temp.averageDistance
        runner.averageDuration=temp.averageDuration
        runner.averageSinuosity=temp.averageSinuosity
        runner.lat=str(temp.averageCenterpoint).split(',')[0].replace('(','').replace(' ','')
        runner.lon=str(temp.averageCenterpoint).split(',')[1].replace(')','').replace(' ','')
        runnerlist.append(runner)
    #request.session['runnerlist']=runnerlist

    return HttpResponse(serializers.serialize('json', runnerlist))