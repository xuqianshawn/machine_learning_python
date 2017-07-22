import json
from geopy.geocoders import Nominatim
from collections import defaultdict
from geopy.distance import vincenty
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
import os
import math


class Points:

    def __init__(self):
        self.longitude = 0
        self.latitude = 0
        self.altitude = 0
        self.hasDistance = False
        self.distance = 0
        self.hasDuration = False
        self.duration = 0
        self.hasSpeed = False
        self.speed = 0
        self.time = ""
        return

    #Load points from json objects
    def load_points_from_json(self, obj):
        hasLong = False
        hasLat = False
        if "longitude" in obj:
            self.longitude = obj["longitude"]
            hasLong = True
        if "latitude" in obj:
            self.latitude = obj["latitude"]
            hasLat = True
        if hasLong is False or hasLat is False:
            return False
        if "distance"in obj:
            self.hasDistance = True
            self.distance = obj["distance"]
        if "duration" in obj:
            self.hasDuration = True
            self.duration = obj["duration"]
        if "speed" in obj:
            self.hasSpeed = True
            self.speed = obj["speed"]
        if "altitude" in obj:
            self.altitude = obj["altitude"]
        if "time" in obj:
            self.time = obj["time"]
        return True



class Session:

    def __init__(self):
        self._id = ""

        self.points = []
        self.centerpoint = (0, 0)
        self.totalDistance = 0
        self.averageSpeed = 0
        self.duration = 0
        self.sinuosity = 0

        self.window_size_factor = 10

        self.hasSpeed = False
        self.hasDuration = False
        self.hasDistance = False

        return

    def length(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def sinuosity(points):
        total = 0
        for i in range(2,len(points)-3):
            l = Session.length(points[i], points[i+1])
            total += l
        straight = points[len(points)-3][0] - points[2][0]
        sin = total / straight
        return sin

    # Load Session from json obj
    def load_from_json(self, obj):
        if "_id" in obj:
            self._id = obj["_id"]
        if "points" in obj:
            # Load all points and its data
            for index in range(0, len(obj["points"])):
                point = Points()
                temp = obj["points"][index]
                if point.load_points_from_json(temp) is True:
                    self.points.append(point)
                    if point.duration > self.duration:
                        self.duration = point.duration
                        self.hasDuration = True

            # Start calculating the averages from loaded data
            tLat = 0
            tLon = 0
            tSpeed = 0
            tDuration = 0
            if len(self.points) != 0:
                for poi in self.points:
                    tLat += poi.latitude
                    tLon += poi.longitude
                    if poi.hasSpeed == True:
                        tSpeed += poi.speed
                        self.hasSpeed = True
                    if poi.hasDistance == True:
                        self.totalDistance += poi.distance
                        self.hasDistance = True
                aLat = tLat / len(self.points)
                aLon = tLon / len(self.points)
                self.averageSpeed = tSpeed / len(self.points)

                self.centerpoint = (aLat, aLon)

                x , y = RBuddy.convert_points_to_plottable(self.points)
                if(len(x) == len(y) and len(y) > 5 and self.hasSpeed):
                    window_size = int(len(y)/self.window_size_factor)
                    poly = 3
                    if window_size % 2 == 0:
                        window_size += 3
                    if window_size == 1:
                        window_size = 3
                    if window_size <= poly:
                        poly = 1
                    #yhat = savgol_filter(y, window_size, poly)
                    yder = savgol_filter(y, window_size, poly, deriv = 1)

                    data_points = []
                    for i in range(0, len(x)):
                        data_points.append((x[i], yder[i]))

                    self.sinuosity = Session.sinuosity(data_points)
            else:
                return False
        return True




class RunnerProfile:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def __init__(self):
        self.user_id = ""

        self.gender = ""
        self.weight = 0
        self.height = 0

        #derived data
        #self.hasSpeed = False
        #self.hasDistance = False
        #self.hasCenterpoint = False
        #self.hasDuration = False
        self.averageSpeed = 0
        self.averageDistance = 0
        self.averageCenterpoint = (0, 0)
        self.averageDuration = 0
        self.averageSinuosity = 0

        self.type = 0       # 0 = Undefined   1 = Casual Jogger     2 = Interval training       3 = Marathoner
        return

    # Load attributes from supplied json obj
    def load_profile_from_json(self, obj):
        if "user_id" in obj:
            self.user_id = obj["user_id"]
        if "gender" in obj:
            self.gender = obj["gender"]
        if "weight" in obj:
            self.weight = obj["weight"]
        if "height" in obj:
            self.height = obj["height"]

class Scorer:

    def __init__(self):
        self.score = 0
        self.wGender = 1
        self.wWeight = 0
        self.wHeight = 0
        self.wDistance = 1
        self.wDuration = 1
        self.wSpeed = 1
        self.wCenterpoint = 1
        self.wType = 3

        self.disCutoff = 50000


    def totalWeight(self):
        return self.wGender + self.wWeight + self.wHeight + self.wDistance + self.wDuration + self.wSpeed + self.wCenterpoint + self.wType

    # Calculate the ratio between two figures, always less than 1
    def calculateRatio(x, y):
        if x == 0 or y == 0:
            return 0
        ratio = x / y
        if ratio > 1:
            ratio = y / x
        return ratio

    # Compare two different user to tell how similar they are
    def compare(self, src, des):
        score = 0
        if src.gender == des.gender:
            score += 1 * self.wGender

        score += Scorer.calculateRatio(src.weight, des.weight) * self.wWeight
        score += Scorer.calculateRatio(src.height, des.height) * self.wHeight
        score += Scorer.calculateRatio(src.averageSpeed, des.averageSpeed) * self.wSpeed
        score += Scorer.calculateRatio(src.averageDistance, des.averageDistance) * self.wDistance
        score += Scorer.calculateRatio(src.averageDuration, des.averageDuration) * self.wDuration

        if src.type == des.type:
            score += 1 * self.wType

        # print(src.averageCenterpoint)
        # print(des.averageCenterpoint)
        distance = vincenty(src.averageCenterpoint, des.averageCenterpoint).meters
        score += 1 - distance / self.disCutoff

        return score / self.totalWeight()

class RBuddy:

    verbose = 1


    def __init__(self):
        self.runners = defaultdict(list)
        self.profiles = defaultdict(RunnerProfile)
        self.jogging_dis_threshold = 5000      #Assume it is in m
        self.sinuosity_jogging_threshold = 1.2
        self.sinuosity_training_threshold = 1.5
        return

    # A logging function for debugging
    def log(self, string):
        if self.verbose > 0:
            print(string)

    # Get top number_of_buddies from ranking list and return it
    def recommend_buddies(self, user, number_of_buddies):
        list = self.get_ranking_list(user)
        user_ids, score = zip(*list)
        new_list = []
        for i in range(0, number_of_buddies):
            if i < len(user_ids):
                new_list.append(user_ids[i])
            else:
                break
        return new_list

    # Get ranking list compared to supplied user
    def get_ranking_list(self, user):
        ranking_list = []
        scorer = Scorer()
        for id in self.profiles:
            if id != user.user_id:
                score = scorer.compare(user, self.profiles[id])
                ranking_list.append((id, score))

        if self.verbose == 2:
            self.log("User location vs Rank 1 location")
            geolocator = Nominatim()
            self.log(str(user.gender))
            location = geolocator.reverse(user.averageCenterpoint)
            self.log(str(location))
            location = geolocator.reverse(self.profiles[ranking_list[0][0]].averageCenterpoint)
            self.log(str(self.profiles[ranking_list[0][0]].gender))
            self.log(str(location))

        return sorted(ranking_list, key=lambda tup:tup[1], reverse = True)

    # Print all gps coordinates into files
    def print_buddies_points_to_file(self, folderpath):
        self.log("Printing buddies points to file now.")
        if not os.path.exists(folderpath):
            self.log(folderpath + " does not exist. Creating now.")
            os.makedirs(folderpath)
        self.log("Printing buddies.")
        for user_id, runner in self.runners.items():
            for session in runner:
                subpath = os.path.join(folderpath, user_id)
                if not os.path.exists(subpath):
                    os.makedirs(subpath)
                fullpath = os.path.join(subpath, session._id)
                file = open(fullpath, 'w')
                for point in session.points:
                    file.write(str(point.latitude) + "," + str(point.longitude) + '\n')
                file.close()
        self.log("Done printing buddies.")

    # Convert the points in x(duration in mins) and y(speed)
    def convert_points_to_plottable(points):
        x = []
        y = []
        dis = 0
        for point in points:
            x.append((point.duration/1000)/60)
            y.append(point.speed)
        return x, y

    # Private function, Calculate thet type of jogger the person is.
    def calculate_type(self, profile):
        # 0 = Undefined   1 = Casual Jogger     2 = Interval training       3 = Marathoner
        if profile.averageDistance >= self.jogging_dis_threshold:
            return 3
        if profile.averageSinuosity == 0:
            return 0
        elif profile.averageSinuosity < 1.2:
            return 1
        else:
            return 2

    # Call this to load buddies into from runners.json
    def load_buddies(self, file_path):
        self.log("Loading buddies from data set.")
        json_file = open(file_path)
        data = []
        for line in json_file:
            data.append(line)

        self.log("Number of session in data set: " + str(len(data)))
        for entry in data:
            obj = json.loads(entry)
            session = Session()
            profile = RunnerProfile()
            profile.load_profile_from_json(obj)
            if session.load_from_json(obj) is True:
                self.runners[profile.user_id].append(session)
            if not profile.user_id in self.profiles:
                self.profiles[profile.user_id] = profile

        for id in self.profiles:
            #did not handle cases of users with no session
            if(len(self.runners[id]) != 0):
                tSpeed = 0
                tDistance = 0
                tDuration = 0
                tLat = 0
                tLon = 0
                tSinu = 0
                for session in self.runners[id]:
                    tSpeed += session.averageSpeed
                    tDistance += session.totalDistance
                    tDuration += session.duration
                    tLat += session.centerpoint[0]
                    tLon += session.centerpoint[1]
                    tSinu += session.sinuosity

                self.profiles[id].averageSpeed = tSpeed / len(self.runners[id])
                self.profiles[id].averageDuration = tDuration / len(self.runners[id])
                self.profiles[id].averageDistance = tDistance / len(self.runners[id])
                self.profiles[id].averageSinuosity = tSinu / len(self.runners[id])

                self.profiles[id].averageCenterpoint = (tLat / len(self.runners[id]), tLon / len(self.runners[id]))
                self.profiles[id].type = self.calculate_type(self.profiles[id])

        self.log("Number of unique buddies in data set: " + str(len(self.profiles)))
        self.log("Done loading buddies from data set.")

    def get_profile(self, id):
        return self.profiles[id]


class MathFunction:
    def __init__(self):
        print('111')
        return
    def length(p0, p1):
        return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

    def sinuosity(points):
        total = 0
        for i in range(2,len(points)-3):
            l = MathFunction.length(points[i], points[i+1])
            total += l
        straight = points[len(points)-3][0] - points[2][0]
        sin = total / straight
        return sin



#rbuddy.print_buddies_points_to_file(".\\Points")

#558fe132a5d2dddb620a316e4955c482
    # file_path = "./mysite/mysite/runners.json"
    # rbuddy = RBuddy()
    # rbuddy.load_buddies(file_path)
    # for id in rbuddy.profiles:
    #    list = rbuddy.recommend_buddies(rbuddy.profiles[id], 10)
    #    break
    # print (list)
    #
    # print(rbuddy.get_profile(list[0]).averageDistance)
    # print(rbuddy.get_profile(list[0]).averageSinuosity)
    # print(rbuddy.get_profile(list[0]).type)