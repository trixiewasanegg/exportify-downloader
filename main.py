
### Imports

import csv
import urllib.request
import re
from pytube import YouTube
import os
from datetime import datetime
import eyed3
import math
import sys

#Gets Timecodes
dateTimeObj = datetime.now()

timestamp = dateTimeObj.strftime("%d-%b-%Y_%H%M")
datestamp = dateTimeObj.strftime("%Y-%m-%d")

###Defines Functions

#Function converts string with Unicode bytes into websafe text
def safeconvert(input):
    output=input.replace(" ", "+")
    output=output.replace(',','')
    output=output.encode('ascii', 'xmlcharrefreplace')
    output=output.decode('ascii')
    return output

#Function gets days between two dates
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


###Gets CSV File from Arguments
try:
    csvin = sys.argv[1]
except:
    csvin = input("Please give the absolute path to your CSV File: \n")    

delim = input('Please Define Your Path Delimiter: \n')

path_prefix = input("Do you want to manually insert a prefix to the path? Leave blank for absolute path \n")


path, file = os.path.split(csvin)

tmp = file.split('.')

playlistname = tmp[0]

###Creates Output Folder

try:
    os.mkdir(os.path.expanduser('~') + delim + 'exportify')
except:
    print ('exportify folder exists')

try:
    dir = os.path.expanduser('~') + delim + 'exportify' + delim + playlistname
    os.mkdir(dir)
except:
    print ("Folder already exists...")



###Actual Code Begins Here

#CSV Import - pulls relevant data from exportify out
with open (csvin, newline='') as testcsv:
    i=0
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
    for row in csv.DictReader(testcsv):
        trnames.append(row['Track Name'])
        arnames.append(row['Artist Name(s)'])
        alnames.append(row['Album Name'])
        trnums.append(row['Track Number'])
        durations.append(row['Track Duration (ms)'])
        print ('Track ', i, ' in playlist as ', row['Track Name'], row ['Artist Name(s)'])
        i=i+1

i=0
for dur in durations:
    dur = int(dur)
    dursec = math.trunc(dur/1000)
    durations[i] = dursec
    i = i+1

#Search YouTube for trname & artist name, stores first video ID in ytids array

i=0
ytresprefix='http://www.youtube.com/results?search_query='
ytpostfix='+Topic'
ytwatchprefix='http://youtube.com/watch?v='
ytids=[]
for trname in trnames:
    print ("Processing item " + str(i+1) + " of " + str(len(trnames)))
    arname = arnames[i]
    alname = alnames[i]
    trnum = trnums[i]
    #Converts CSV Output into Websafe Queries
    trnamesafe=safeconvert(trname)
    arnamesafe=safeconvert(arname)

    #Concatenates into query
    query=ytresprefix + trnamesafe + '+' + arnamesafe + ytpostfix
    print ('Querying ' + query)

    #Queries YouTube Search Results - returns first result
    html = urllib.request.urlopen(query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    id=video_ids[0]
    ytids.append(id)

    #Generates URL and Filename variables
    url=ytwatchprefix + id
    filename=id + '.mp4'
    yt = YouTube(url)

    #Downloads ID
    print ('Downloading ' + url + '...')
    stream = yt.streams.get_audio_only()
    stream.download(filename=filename,output_path=dir)

    #ffmpeg imports from filein and exports to fileout
    fileout = dir + delim + id + '.mp3'
    filein = dir + delim + id + '.mp4'
    print ('Converting ' + filein + ' to ' + fileout)
    cmd = 'ffmpeg -hide_banner -loglevel error -i  ' + filein +' ' + fileout
    os.system(cmd)

    #Writes Metadata
    print ('Writing meta to ' + fileout)
    meta = eyed3.load(fileout)
    meta.tag.artist = arname
    print ('Artist: ' + arname)
    meta.tag.title = trname
    print ('Track: ' + trname)
    meta.tag.album = alname
    print ('Album: ' + alname)
    meta.tag.track_num = int(trnum)
    print ('Track Number: ' + trnum)
    meta.tag.save()
    print ('Meta Saved.')
    i=i+1
    print ('Cleaning Up')
    os.remove(filein)

print ("Generating tab separated .txt file for iTunes to read")
tsv = dir + '/' + playlistname + '.txt'
with open(tsv, 'wt', newline='') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['Name', 'Artist', 'Composer', 'Album', 'Grouping', 'Work', 'Movement Number', 'Movement Count', 'Movement Name', 'Genre', 'Size', 'Time', 'Disc Number', 'Disc Count', 'Track Number', 'Track Count', 'Year', 'Date Modified', 'Date Added', 'Bit Rate', 'Sample Rate', 'Volume Adjustment', 'Kind', 'Equaliser', 'Comments', 'Plays', 'Last Played', 'Skips', 'Last Skipped', 'My Rating', 'Location'])
    i=0
    bitrate=128
    samplerate=44100
    dateadd=days_between(datestamp, '1900-01-01')
    kind='MPEG audio file'
    for trname in trnames:
        arname=arnames[i]
        alname=alnames[i]
        trnum=trnums[i]
        dur=durations[i]
        id=ytids[i]
        fileout = dir + delim + id + '.mp3'
        size = os.path.getsize(fileout)
        if path_prefix == '':
            path = os.path.abspath(fileout)
        else:
            path = path_prefix + delim + playlistname + delim + id
        print ('Written row ' + str(i))
        tsv_writer.writerow([trname, arname, '', alname, '', '', '', '', '', '', size, dur, '', '', trnum, '', '', dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', path])
        i = i+1