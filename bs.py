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
locationfail=[]
#Playlist Name
playlistnames=[]
#Sizes
sizes=[]

inputfolder = 'C:\\Users\\hi\\Documents\\GitHub\\exportify-to-itunes\\tsv to fix\\'

foldercontents = os.listdir(inputfolder)

outputfolder = 'C:\\Users\\hi\\Documents\\GitHub\\exportify-to-itunes\\tsvout\\'

path = 'Macintosh HD/Users/bea/Music/Music/Media.localized/Music'

delim = '/'

for tsvin in foldercontents:
    tmp = tsvin.split('.')
    playlistname = tmp[0]
    print (playlistname)
    file = inputfolder + playlistname + '.txt'
    with open(file, newline='') as input:
        for row in csv.DictReader(input, delimiter='\t'):
            trname = row['Name']
            trnames.append(trname)
            arname = row['Artist']
            arnames.append(arname)
            alname = row['Album']
            alnames.append(alname)
            trnum = row['Track Number']
            trnums.append(trnum)
            durtmp = row['Time']
            dur = int(durtmp)/2
            durations.append(dur)
            sizes.append(row['Size'])
            if int(trnum) == 10:
                relpth = arname + delim + alname + delim + trnum + ' ' + trname + '.mp3'
            if int(trnum) > 10:
                relpth = arname + delim + alname + delim + trnum + ' ' + trname + '.mp3'
            else:
                trnum = '0' + trnum
                relpth = arname + delim + alname + delim + trnum + ' ' + trname + '.mp3'
            location = path + delim + relpth
            locations.append(location)
            
    i=0
    tsv = outputfolder + playlistname + '.txt'
    with open(tsv, 'wt', newline='') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Name', 'Artist', 'Composer', 'Album', 'Grouping', 'Work', 'Movement Number', 'Movement Count', 'Movement Name', 'Genre', 'Size', 'Time', 'Disc Number', 'Disc Count', 'Track Number', 'Track Count', 'Year', 'Date Modified', 'Date Added', 'Bit Rate', 'Sample Rate', 'Volume Adjustment', 'Kind', 'Equaliser', 'Comments', 'Plays', 'Last Played', 'Skips', 'Last Skipped', 'My Rating', 'Location'])
        while i < len(trnames):
                trname = trnames[i]
                arname = arnames[i]
                alname = alnames[i]
                trnum = trnums[i]
                dur = durations[i]
                location = locations[i]
                size = sizes[i]
                
                dateadd='44505'

                #Defines Consistent Variables
                bitrate=128
                samplerate=44100
                kind='MPEG audio file'
                tsv_writer.writerow([trname, arname, '', '', '', '', '', '', '', '', size, dur, '', '', trnum, '', '', dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', location])
                i = i+1
    trnames=[]
    arnames=[]
    alnames=[]
    trnums=[]
    durations=[]
    ytids=[]
    locations=[]
    playlistnames=[]
    sizes=[]