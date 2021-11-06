import csv
from datetime import datetime
import os
import math

dateTimeObj = datetime.now()

timestamp = dateTimeObj.strftime("%d-%b-%Y_%H%M")
datestamp = dateTimeObj.strftime("%Y-%m-%d")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

os.mkdir(timestamp)

tsv = timestamp + '/playlist.txt'

with open ('testcsv2.csv', newline='') as testcsv:
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
    #YTIDS
    ytids=[]
    for row in csv.DictReader(testcsv):
        ytids.append(row['Popularity'])
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

with open(tsv, 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['Name', 'Artist', 'Composer', 'Album', 'Grouping', 'Work', 'Movement Number', 'Movement Count', 'Movement Name', 'Genre', 'Size', 'Time', 'Disc Number', 'Disc Count', 'Track Number', 'Track Count', 'Year', 'Date Modified', 'Date Added', 'Bit Rate', 'Sample Rate', 'Volume Adjustment', 'Kind', 'Equaliser', 'Comments', 'Plays', 'Last Played', 'Skips', 'Last Skipped', 'My Rating', 'Location'])
    i=0
    bitrate=128
    samplerate=44100
    dateadd=days_between(datestamp, '1900-01-01')
    #Get the Size of the File Somehow
    size=69
    kind='MPEG audio file'
    for trname in trnames:
        arname=arnames[i]
        alname=alnames[i]
        trnum=trnums[i]
        dur=durations[i]
        id=ytids[i]
        path = 'C:\\Users\\hi\\Music\\iTunes\\iTunes Media\\Music\\' + arname + '\\' + alname + '\\' + id + '.mp3'
        tsv_writer.writerow([trname, arname, '', alname, '', '', '', '', '', '', size, dur, '', '', trnum, '', '', dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', path])
import csv
from datetime import datetime
import os
import math

dateTimeObj = datetime.now()

timestamp = dateTimeObj.strftime("%d-%b-%Y_%H%M")
datestamp = dateTimeObj.strftime("%Y-%m-%d")

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

os.mkdir(timestamp)

tsv = timestamp + '/playlist.txt'

with open ('testcsv2.csv', newline='') as testcsv:
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
    #YTIDS
    ytids=[]
    for row in csv.DictReader(testcsv):
        ytids.append(row['Popularity'])
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

with open(tsv, 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(['Name', 'Artist', 'Composer', 'Album', 'Grouping', 'Work', 'Movement Number', 'Movement Count', 'Movement Name', 'Genre', 'Size', 'Time', 'Disc Number', 'Disc Count', 'Track Number', 'Track Count', 'Year', 'Date Modified', 'Date Added', 'Bit Rate', 'Sample Rate', 'Volume Adjustment', 'Kind', 'Equaliser', 'Comments', 'Plays', 'Last Played', 'Skips', 'Last Skipped', 'My Rating', 'Location'])
    i=0
    bitrate=128
    samplerate=44100
    dateadd=days_between(datestamp, '1900-01-01')
    #Get the Size of the File Somehow
    size=69
    kind='MPEG audio file'
    for trname in trnames:
        arname=arnames[i]
        alname=alnames[i]
        trnum=trnums[i]
        dur=durations[i]
        id=ytids[i]
        path = 'C:\\Users\\hi\\Music\\iTunes\\iTunes Media\\Music\\' + arname + '\\' + alname + '\\' + id + '.mp3'
        tsv_writer.writerow([trname, arname, '', alname, '', '', '', '', '', '', size, dur, '', '', trnum, '', '', dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', path])
        i = i+1