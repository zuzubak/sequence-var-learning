# assign a google cloud api key to the variable 'api_key' before running.
# call avg_ratio(). Input arguments:
#       1. list of [lat,long] coordinates that form a polygon within which to perform the calculation.
#       2. number of observations to make (how many random pairs of points to test).
#       3. (optional) minimum journey distance, in metres (defaults to zero)
#       4. (optional) maximum journey distance, in metres (defaults to 1000000000)
# Result is the average ratio between the distance as the crow flies and 'as the human walks';
# Lower values (closer to 1) indicate more efficient street systems, higher values less efficient.

import re
import urllib
import random
import numpy as np
import math
import json
from math import sin, cos, sqrt, atan2
from collections import OrderedDict
from urllib import request
from urllib.request import urlopen
import shapely
from shapely import geometry
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

pattern1=re.compile("[0-9]{1,3}(.[0-9])? k?m")
api_key='AIzaSyA9zpgz98E5BieMwxU6EdC37B0rxGb2PvY'
base_url='https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=12.3456789,-22.3456789&destinations=32.3456789%2C-42.3456789%7C&mode=walking&key='+api_key


def get_dist(point_a,point_b): #get shortest walking distance from point A [lat-coord, long-coord] to point B.
    new_url=base_url[0:78]+str(point_a[0])+','+str(point_a[1])+base_url[100:114]+str(point_b[0])+','+str(point_b[1])+base_url[141:]
    with urllib.request.urlopen(new_url) as response:
        jdict=json.loads(response.read())
    print(jdict)
    result=''
    if jdict['rows'][0]['elements'][0]['status']=='ZERO_RESULTS':
        result=None
    else:
        result=jdict['rows'][0]['elements'][0]['distance']['value']
    return result 

def ll_to_m(point_a,point_b): #calculate distance in metres between two coordinate points.
    R = 6373000 #Radius of the earth in metres
    lat1 = math.radians(point_a[0])
    lon1 = math.radians(point_a[1])
    lat2 = math.radians(point_b[0])
    lon2 = math.radians(point_b[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def avg_ratio(i_polygon_list,n_observations,min_dist=0,max_dist=1000000000):
    ratio_list=[]
    polygon_list=[]
    for item in i_polygon_list:
        polygon_list.append([item[0],item[1]])
    print(polygon_list)
    polygon=Polygon(polygon_list)
    lat_list=[]
    long_list=[]
    for item in polygon_list:
        lat_list.append(item[0])
    for item in polygon_list:
        long_list.append(item[1])
    minlat=min(lat_list)
    minlong=min(long_list)
    maxlat=max(lat_list)
    maxlong=max(long_list)
    latm=maxlat-minlat
    longm=maxlong-minlong
    i=0
    while i<n_observations:
        r1_lat=minlat+latm*random.random()
        r1_long=minlong+longm*random.random()
        r2_lat=minlat+latm*random.random()
        r2_long=minlong+longm*random.random()
        start_point=[r1_lat,r1_long]
        end_point=[r2_lat,r2_long]
        if polygon.contains(Point(start_point))==True and polygon.contains(Point(end_point))==True:
            straight=ll_to_m(start_point,end_point)
            if straight>min_dist and straight<max_dist:
                windy=get_dist(start_point,end_point)
                if type(windy) is int:
                    print('YYYYYYYY')
                    ratio_list.append(float(windy)/straight)
                    print(windy/straight)
                    i+=1
                    print(i)
    return sum(ratio_list)/len(ratio_list)

