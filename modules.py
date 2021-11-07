import csv
import math
import os
import re
import urllib.request
from datetime import datetime
import eyed3
from pytube import YouTube

###Functions

#Converts String into Websafe ASCII
def safeconvert(input):
    output=input.replace(" ", "+")
    output=output.replace(',','')
    output=output.encode('ascii', 'xmlcharrefreplace')
    output=output.decode('ascii')
    return output

#Queries Youtube for Track/Artist, outputs first result as YouTube ID
def ytquery(trname, arname):
    #Prefix for YouTube Results
    ytresprefix='http://www.youtube.com/results?search_query='
    #Any Postfix for Search
    searchpostfix='+Topic'

    #Converts input variables into ASCII
    trnamesafe = safeconvert(trname)
    arnamesafe = safeconvert(arname)

    #Concatenates Query
    query=ytresprefix + trnamesafe + '+' + arnamesafe + searchpostfix
    print ('Querying ' + query)

    #Queries YouTube
    html = urllib.request.urlopen(query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    id=video_ids[0]

    #Returns ID
    print ('Returned ' + id)
    return id

#Downloads YouTube ID into Directory, Path Delimiter Defined
def ytdown(id, dir, delim):
    #Defines Watch Prefix
    ytwatchprefix='http://youtube.com/watch?v='

    #Defines URL and opens in YouTube
    url = ytwatchprefix + id   
    yt = YouTube(url)

    #Downloads File
    filename = id + '.mp4'
    print ('Downloading ' + url + '...')
    stream = yt.streams.get_audio_only()
    stream.download(filename=filename,output_path=dir)

    #ffmpeg imports from filein and exports to fileout
    fileout = dir + delim + id + '.mp3'
    filein = dir + delim + id + '.mp4'
    print ('Converting ' + filein + ' to ' + fileout)
    cmd = 'ffmpeg -hide_banner -loglevel error -y -i  ' + filein +' ' + fileout
    os.system(cmd)

    #Deletes File In
    print ('Cleaning Up')
    os.remove(filein)

    return fileout

#Writes ID3 Metadata to file
def meta(file, arname, trname, alname, trnum):
    print ('Writing meta to ' + file)
    meta = eyed3.load(file)
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

#Days Between Generator
def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#Primary Playlist Making Function
def makeplaylist(csvin, delim, path_prefix, dir, playlistname):
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

    ###CSV Import into Lists
    with open (csvin, newline='') as input:
        i=0
        for row in csv.DictReader(input):
            trnames.append(row['Track Name'])
            arnames.append(row['Artist Name(s)'])
            alnames.append(row['Album Name'])
            trnums.append(row['Track Number'])
            dur = int(row['Track Duration (ms)'])
            dursec = math.trunc(dur/1000)
            durations.append(str(dursec))
    
    ###Runs through lists, generates YouTube IDs, downloads them, converts to mp3 and adds id3 meta
    i=0
    while i < len(trnames):
        #Defines Relevant Variables from Lists
        track = trnames[i]
        artist = arnames[i]
        album = alnames[i]
        trnum = trnums[i]

        #Queries YouTube and Appends to ytids
        ytid = ytquery(track, artist)
        ytids.append(ytid)
        
        #Downloads Stream
        try:
            fileout = ytdown(ytid, dir, delim)
            meta(fileout, artist, track, album, trnum)
        
        except:
            text = ytid + ' error occured when downloading - playlist:' + playlistname
            exception('400', text, delim)
        i = i+1
    
    ###Generates TSV for iTunes to read
    print ("Generating tab separated .txt file for iTunes to read")

    #Defines File
    tsv = dir + delim + playlistname + '.txt'

    #Opens file
    with open(tsv, 'wt', newline='') as out_file:
        
        #Defines delimiter and headers
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(['Name', 'Artist', 'Composer', 'Album', 'Grouping', 'Work', 'Movement Number', 'Movement Count', 'Movement Name', 'Genre', 'Size', 'Time', 'Disc Number', 'Disc Count', 'Track Number', 'Track Count', 'Year', 'Date Modified', 'Date Added', 'Bit Rate', 'Sample Rate', 'Volume Adjustment', 'Kind', 'Equaliser', 'Comments', 'Plays', 'Last Played', 'Skips', 'Last Skipped', 'My Rating', 'Location'])
        
        #Generates Dateadded
        dateTimeObj = datetime.now()
        datestamp = dateTimeObj.strftime("%Y-%m-%d")
        dateadd=days_between(datestamp, '1900-01-01')

        #Defines Consistent Variables
        bitrate=128
        samplerate=44100
        kind='MPEG audio file'

        #Loops through lists, writing to TSV
        i=0
        while i < len(trnames):
            trname = trnames[i]
            arname=arnames[i]
            alname=alnames[i]
            trnum=trnums[i]
            dur=durations[i]
            id=ytids[i]
            fileout = dir + delim + id + '.mp3'
            try:
                size = os.path.getsize(fileout)
            except:
                exception('404', 'failed to get size of file ' + fileout, delim)
                size = str(0)
            if path_prefix == '':
                path = os.path.abspath(fileout)
            else:
                path = path_prefix + delim + playlistname + delim + id
            print ('Written row ' + str(i))
            tsv_writer.writerow([trname, arname, '', alname, '', '', '', '', '', '', size, dur, '', '', trnum, '', '', dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', path])
            i = i+1

#Exception Handler
def exception(code, text, delim):
    if delim == '':
        delim = "\\"
    print ("Oh shit, something went wrong... Lemme just document this")
    file = os.path.expanduser('~') + delim + 'playlists' + delim + 'exceptions.csv'
    dateTimeObj = datetime.now()
    timecode = dateTimeObj.strftime("%Y-%m-%d_%H%M")
    with open(file, 'a', newline='') as excfile:
        csv_writer = csv.writer(excfile, delimiter=',')
        csv_writer.writerow([timecode, code, text])
    print ("Documented: " +timecode + ', ' + code + ', ' + text)