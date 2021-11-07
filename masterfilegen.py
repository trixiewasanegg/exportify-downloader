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
#Locations
locations=[]
#Playlist Name
playlistnames=[]
#Key
key=[]

outputfolder = 'C:\\Users\\hi\\Documents\\GitHub\\exportify-to-itunes\\tsvout'

inputfolder = 'C:\\Users\\hi\\Documents\\GitHub\\exportify-to-itunes\\tsv to fix\\'

foldercontents = os.listdir(inputfolder)

for tsvin in foldercontents:
    tmp = tsvin.split('.')
    playlistname = tmp[0]
    print (playlistname)
    file = inputfolder + playlistname + '.txt'
    with open(file, newline='') as input:
        for row in csv.DictReader(input, delimiter='\t'):
            trnames.append(row['Name'])
            arnames.append(row['Artist'])
            alnames.append(row['Album'])
            trnums.append(row['Track Number'])
            durtmp = row['Time']
            dur = int(durtmp)/2
            durations.append(dur)
            locations.append(row['Location'])
    i=0
    tsv = outputfolder + 'master.csv'
    with open(tsv, 'wt', newline='') as out_file:
        csv_writer = csv.writer(out_file, delimiter=',')
        csv_writer.writerow(['Key', 'Artist', 'Track', 'Album', 'TrackNum', 'Duration', 'Location'])
        while i < len(trnames):
                trname = trnames[i]
                arname = arnames[i]
                alname = alnames[i]
                trnum = trnums[i]
                dur = durations[i]
                location = locations[i]
                key = safeconvert(trname) + safeconvert(arname)
                csv_writer.writerow([key, arname, trname, alname, trnum, dur, location])
                i = i+1