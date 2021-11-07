import csv
import os
from modules import safeconvert

###Defines Arrays for Usage
#Track Name
trnames=[]
#Artist Name
arnames=[]
#Album Name
alnames=[]
#Track Numbers
trnums=[]
#Duration
durations=[]
#YouTube IDs (will be used as file-names)
ytids=[]
#Keys
keys=[]
#Locations
locations=[]
#Playlist Name
playlistnames=[]

with open('master.csv', newline='') as master:
    for row in csv.DictReader(master, delimiter=','):
        keys.append(row['Key'])
        locations.append(row['Location'])

key = 'Get+LemonDisciple'

a = keys.index(key)
location = locations[a]

print (location)