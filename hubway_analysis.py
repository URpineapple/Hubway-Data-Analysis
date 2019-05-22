import pandas as pd
import numpy as np
import csv
from pandas import *
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from datetime import timedelta
from math import sin, cos, sqrt, atan2, radians

def isMale(row):
    if row['gender'] == 'Male':
        return 1
    return 0

def isFemale(row):
    if row['gender'] == 'Female':
        return 1
    return 0

def latitude(sta_set, sta):
    return sta_set.loc[sta, 'lat']

def longtitude(sta_set, sta):
    return sta_set.loc[sta, 'lng']

def distance(start, finish, sta_set):
    R = 6373.0

    lat1 = radians(latitude(sta_set, start))
    lon1 = radians(longtitude(sta_set, start))
    lat2 = radians(latitude(sta_set, finish))
    lon2 = radians(longtitude(sta_set, finish))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance*1000

def getYear (row):
    return row['end_date'].year




"""
Import Data
"""
# if "header = None", then the header will be included in the daraset
dataset = read_csv('hubway_trips.csv')
stationset = read_csv('hubway_stations.csv')
s1 = stationset.set_index('id')

"""
Preprocessing
"""
# get rid of rows whose 'gender' section is NaN
df = dataset.dropna(subset=['gender'])

# Remove rows whose 'end_statn' section is NaN
df = df.dropna(subset=['strt_statn'])
df = df.dropna(subset=['end_statn'])
df = df.dropna(subset=['birth_date'])

# remove rows whose duration is not in the range of 60-86400
# the '& 'is a logic operator here
# the parenthesis is used so that two conditions can both be applied
df = df[(df['duration'] >= 60) & (df['duration'] <= 86400)]# remove rows whose start station ans end station are the same one
df = df[(df['strt_statn'] != df['end_statn'])]


"""
Generate new columns
"""
df = df.set_index('seq_id')

df['distance'] = df.apply(lambda x: distance(x.strt_statn, x.end_statn, stationset), axis=1)

df['speed'] = (df['distance']/df['duration'])*3.6

df['Male'] = df.apply(lambda row: isMale(row), axis=1)
df['Female'] = df.apply(lambda row: isFemale(row), axis=1)

df['end_date'] = pd.to_datetime(df['end_date'])
df['year'] = df.apply(lambda row: getYear(row), axis =1)
df['age'] = df['year'] - df['birth_date']
print("This is df1", df)

"""
boxplot1 = dataset.boxplot(column=['duration'], fontsize=10)
plt.xlabel('before')
plt.ylabel('Value')
plt.savefig('fig1.png')
#plt.show()

boxplot2 = df1.boxplot(column=['duration'], fontsize=10)
plt.xlabel('After')
plt.ylabel('Value')
plt.savefig('fig2.png')
#plt.show()
"""


# For the convenience of analysis, we only get the data sample of size 100
d1 = df.head(100)
"""
d1 = d1.set_index('seq_id')

print('Here \'s the dataset sample 1: ')
print(d1)

# The code below will generate a new column 'distance',
# which is based on each trip's start station and end station
d1['distance'] = d1.apply(lambda x: distance(x.strt_statn, x.end_statn, s1), axis=1)


# Convert the speed from m/s to km/h
d1['speed'] = (d1['distance']/d1['duration'])*3.6


# These codes below generates two new columns
# which tell whether the trip's user is Males or Female
d1['Male'] = d1.apply(lambda row: isMale(row), axis=1)
d1['Female'] = d1.apply(lambda row: isFemale(row), axis=1)
"""

"""
Visualize the relationship between speed and age
"""
# d2 = df[['birth_date', 'speed']]
d2 = d1[['age', 'speed']]
d2 = d2.groupby(['age']).mean()
plot1 = d2.plot(figsize=(16, 9))
plot1.set_xlabel("Age", fontsize=16)
plot1.set_ylabel("Average Speed", fontsize=16)
plot1.set_title("Line Plot for Age and Speed", fontweight="bold", fontsize=20)
plt.savefig('Result1.png')
plt.show()

"""
x1 = d1['birth_date']
y1 = d1['speed']
fig1 = plt.figure(figsize=(16,9))
plt.plot(x1, y1)
plt.xlabel("birth_date")
plt.ylabel("speed")
plt.title("Plot1")
fig1.savefig('Fig1.png', dpi=100)
plt.figure(figsize=(16,9))
plt.show()
"""

"""
Visualize the relationship between speed and gender
"""
# d2 = d1.loc[d1['gender']=='Female', 'speed', 'birth_date']

# d3 = d1[d1['gender'] == 'Female']
d3 = df[df['gender'] == 'Male']
d3 = d3[['age', 'speed']]
d3 = d3.groupby(['age']).mean()
ax = d3.plot(figsize=(16, 9))

# d4 = d1[d1['gender'] == 'Male']
d4 = df[df['gender'] == 'Female']
d4 = d4[['age', 'speed']]
d4 = d4.groupby(['age']).mean()
d4.plot(ax=ax, figsize=(16, 9))

plt.xlabel("Birth Date", fontsize=16)
plt.ylabel("Average Speed", fontsize=16)
plt.title("Line Plot for Gender and Speed", fontweight="bold", fontsize=20)
plt.legend(["Male", "Female"])
plt.savefig('Result2.png')
plt.show()

"""
#d4 = d4.reset_index()
plot3 = d3.plot.line()
#d3.plot(x=d3['birth_date'], y=d3['speed'])
#plt.plot(x=d4['birth_date'], y=d4['speed'])
#plt.show()
"""


"""
Visualize the relationship between start station and gender
"""
# d5 = d1[['strt_statn', 'Male', 'Female']]
d5 = df[['strt_statn', 'Male', 'Female']]
bstation = d5['strt_statn']
d5 ['strt_statn'] = bstation.astype(int)
d5 = d5.groupby(['strt_statn']).sum()

plot1 = d5.plot.bar(stacked=True, figsize=(32, 9))
plot1.set_xlabel("Start Station ID", fontsize=16)
plot1.set_ylabel("User Count", fontsize=16)
plot1.set_title("Stacked Bar Plot for Gender and Start Station", fontweight="bold", fontsize=20)
plt.xticks(rotation=30, fontsize=10)
plt.savefig('Result3.png')
plt.show()

"""
Visualize the relationship between end station and gender
"""
# d6 = d1[['end_statn', 'Male', 'Female']]
d6 = df[['end_statn', 'Male', 'Female']]
bstation = d6['end_statn']
d6 ['end_statn'] = bstation.astype(int)
d6 = d6.groupby(['end_statn']).sum()

plot2 = d6.plot.bar(stacked=True, figsize=(32, 9))
plot2.set_xlabel("End Station ID", fontsize=16)
plot2.set_ylabel("User Count", fontsize=16)
plot2.set_title("Stacked Bar Plot for Gender and End Station", fontweight="bold", fontsize=20)
plt.xticks(rotation=30, fontsize=10)
plt.savefig('Result4.png')
plt.show()



"""
d2 = d1[['strt_statn', 'Male', 'Female']]
d2 = d2.groupby(['strt_statn']).sum()
d2.to_csv('HW5.csv')

plot1 = d2.plot.bar()
plot1.set_xlabel("Start Station")
plot1.set_ylabel("Number")
plot1.set_title("Side-by-Side Bars")
plt.savefig('NO1.png')
plt.show()

plot2 = d2.plot.bar(stacked=True)
plot2.set_xlabel("Start Station")
plot2.set_ylabel("Number")
plot2.set_title("Stack Bars")
plt.savefig('NO2.png')
plt.show()

plot3 = d2.plot.line()
plot3.set_xlabel("Start Station")
plot3.set_ylabel("Number")
plot3.set_title("Line Chart")
plt.savefig('NO3.png')
plt.show()

plot4 = d2.plot.kde()
plot4.set_title("Density Plot")
plt.savefig('NO4.png')
plt.show()
"""
