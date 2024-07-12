import csv
import math
import os
from datetime import datetime
import eyed3
from pytube import YouTube
from pytube import Search

###Functions

#Converts String into Websafe ASCII
def safeconvert(input):
    output=input.replace(" ", "+")
    output=output.replace("ö","o")
    output=output.encode('ascii', 'xmlcharrefreplace')
    output=output.decode('ascii')
    output=output.replace(',','')
    output=output.replace("&","+")
    return output

#Queries Youtube for Track/Artist, outputs first result as YouTube ID
def ytquery(trname, arname):
    #Generates the search query as Artist Track + Topic bc YouTube Music
    query = trname + " " + arname + " Topic"
    print("Querying " + query)
    #Tells pytube to query
    s = Search(query)
    #Grabs the first ID and returns it.
    id = str(s.results[0])[41:52]
    print("Returned ID " + id)
    return id

#Downloads YouTube ID into Directory, Path Delimiter Defined
def ytdown(id, dir, delim, file):
    #Defines Watch Prefix
    ytwatchprefix='https://youtu.be/'

    #Defines URL and opens in YouTube
    url = ytwatchprefix + id   
    yt = YouTube(url)

    #Downloads File
    filename = file + '.mp4'
    print ('Downloading ' + url + '...')
    stream = yt.streams.get_audio_only().download(filename=filename,output_path=dir)

    #ffmpeg imports from filein and exports to fileout
    fileout = dir + delim + file + '.mp3'
    filein = dir + delim + filename
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

#Takes Keys and turns it into Mixed In Key Camelot Code
def keycalc(key,mode):
    #Defines Key Arrays
    #Look, I fucking hate this too but this is the easiest way I could think of doing it without learning music theory
    minor_key = ['5A','12A','7A','2A','9A','4A','11A','6A','1A','8A','3A','10A']
    major_key = ['8B','3B','10B','5B','12B','7B','2B','9B','4B','11B','6B','1B']

    if mode == 0:
        return(minor_key[key])
    if mode == 1:
        return(major_key[key])

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
    #YouTube IDs
    ytids=[]
    #FileNames
    filenames=[]
    #Genres
    genres=[]
    #Year
    years=[]

    ###CSV Import into Lists
    with open (csvin, newline='') as input:
        i=0
        for row in csv.DictReader(input):
            trnames.append(row['Track Name'])
            track = row['Track Name']
            arnames.append(row['Artist Name(s)'])
            artist = row['Artist Name(s)']
            filenames.append(safeconvert(artist+"_"+track))
            alnames.append(row['Album Name'])
            # Current version of exportify doesn't include track nums, defined as 1
            # trnums.append(row['Track Number'])
            trnums.append('1')
            dur = int(row['Duration (ms)'])
            dursec = math.trunc(dur/2000)
            durations.append(str(dursec))
            genres.append(safeconvert(row['Genres'].split(',')[0]))
            years.append(str(row['Release Date'].split('-')[0]))

    
    ###Runs through lists, generates YouTube IDs, downloads them, converts to mp3 and adds id3 meta
    i=0
    while i < len(trnames):
        #Defines Relevant Variables from Lists
        track = trnames[i]
        artist = arnames[i]
        album = alnames[i]
        trnum = trnums[i]
        genre = genres[i]
        year = years[i]
        filename = filenames[i]
        #Queries YouTube and Appends to ytids
        ytid = ytquery(track, artist)
        ytids.append(ytid)
        
        #Downloads Stream
        try:
            fileout = ytdown(ytid, dir, delim, filename)
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
            filename=filenames[i]
            fileout = dir + delim + filename + '.mp3'
            try:
                size = os.path.getsize(fileout)
            except:
                exception('404', 'failed to get size of file ' + fileout, delim)
                size = str(0)
            if path_prefix == '' or path_prefix == 0:
                path = os.path.abspath(fileout)
            else:
                path = path_prefix + delim + playlistname + delim + id
            print ('Written row ' + str(i))
            tsv_writer.writerow([trname, arname, '', alname, '', '', '', '', '', genre, size, dur, '', '', trnum, '', year, dateadd, dateadd, bitrate, samplerate, '', kind, '', '', '', '', '', '', '', path])
            i = i+1

#DJ Playlist Maker
def makeDJPlaylist(csvin, delim, dir, playlistname):
    ###Defines Arrays for Usage
    #Track Name
    trnames=[]
    #Artist Name
    arnames=[]
    #Key
    keys=[]
    #Tempo
    tempos=[]
    #Genres
    genres=[]
    #YouTube IDs (will be used as file-names)
    ytids=[]

    ###CSV Import into Lists
    with open (csvin, newline='') as input:
        i=0
        for row in csv.DictReader(input):
            #Artist & Track name
            trnames.append(row['Track Name'])
            arnames.append(row['Artist Name(s)'])
            #Finds Camelot Key
            key = keycalc(int(row['Key']),int(row['Mode']))
            keys.append(key)
            #Rounds Tempo to nearest whole num
            tempo = round(float(row['Tempo']),0)
            tempos.append(str(tempo).split('.')[0])
            #Finds Genres
            genres.append(safeconvert(row['Genres'].split(',')[0]))

    ###Runs through lists, generates YouTube IDs, downloads them & converts to mp3
    i=0
    while i < len(trnames):
        #Defines Relevant Variables from Lists
        track = trnames[i]
        artist = arnames[i]
        tempo = tempos[i]
        key = keys[i]
        genre = genres[i]
        filename = safeconvert("["+key+'_'+tempo+'_'+genre+"]"+artist+'-'+track)

        #Queries YouTube and Appends to ytids
        ytid = ytquery(track, artist)
        ytids.append(ytid)
        
        #Downloads Stream
        try:
            fileout = ytdown(ytid, dir, delim, filename)
            print('Finished '+fileout)
        
        except:
            text = ytid + ' error occured when downloading - playlist:' + playlistname
            exception('400', text, delim)
        i = i+1    

#Pure Downloader
def pureDownload(csvin, delim, dir, playlistname):
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
    #YouTube IDs
    ytids=[]
    #FileNames
    filenames=[]
    #Genres
    genres=[]
    #Year
    years=[]

    ###CSV Import into Lists
    with open (csvin, newline='') as input:
        i=0
        for row in csv.DictReader(input):
            trnames.append(row['Track Name'])
            track = row['Track Name']
            arnames.append(row['Artist Name(s)'])
            artist = row['Artist Name(s)']
            filenames.append(safeconvert(artist+"_"+track))
            alnames.append(row['Album Name'])
            # Current version of exportify doesn't include track nums, defined as 1
            # trnums.append(row['Track Number'])
            trnums.append('1')
            dur = int(row['Duration (ms)'])
            dursec = math.trunc(dur/2000)
            durations.append(str(dursec))
            genres.append(safeconvert(row['Genres'].split(',')[0]))
            years.append(str(row['Release Date'].split('-')[0]))

    
    ###Runs through lists, generates YouTube IDs, downloads them, converts to mp3 and adds id3 meta
    i=0
    while i < len(trnames):
        #Defines Relevant Variables from Lists
        track = trnames[i]
        artist = arnames[i]
        album = alnames[i]
        trnum = trnums[i]
        filename = filenames[i]
        #Queries YouTube and Appends to ytids
        ytid = ytquery(track, artist)
        ytids.append(ytid)
        
        #Downloads Stream
        try:
            fileout = ytdown(ytid, dir, delim, filename)
            meta(fileout, artist, track, album, trnum)
        
        except:
            text = ytid + ' error occured when downloading - playlist:' + playlistname
            exception('400', text, delim)
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