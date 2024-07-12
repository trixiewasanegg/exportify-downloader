from modules import safeconvert
from modules import makeplaylist
from modules import makeDJPlaylist
from modules import pureDownload
import sys
import os

###Gets CSV File from Arguments
try:
    csvin = sys.argv[1]
except:
    csvin = input("Please give the absolute path to your CSV File: \n")

###Defines Delimiter
delim = input('Please Define Your Path Delimiter: \n')

###Defines Playlist Name
playlistname = input("What should I call this playlist? \n")

directory = safeconvert(playlistname)

###Creates Output Folder/s
try:
    os.mkdir(os.path.expanduser('~') + delim + 'playlists')
except: 
    print ('Playlists folder exists')

try:
    dir = os.path.expanduser('~') + delim + 'playlists' + delim + directory
    os.mkdir(dir)
except:
    print ("Folder already exists...")

brk = 0

###Defines Use Case (see readme for breakdown)
while brk != 1:
    usage = input("Please select use case: \n 1: Porting Spotify Playlist to iTunes \n 2: Downloading tracks to mix\n 3: Pure Download\n")
    usage = int(usage)
    if usage == 1:
        ###Defines Path Prefix
        path_prefix = input("Do you want to insert path for iTunes to read? Leave blank for absolute path \n")
        if path_prefix == '':
            path_prefix = 0
        makeplaylist(csvin, delim, path_prefix, dir, playlistname)
        brk = 1
    elif usage == 2:
        makeDJPlaylist(csvin, delim, dir, playlistname)
        brk = 1
    elif usage == 3:
        pureDownload(csvin, delim, dir, playlistname)
        brk = 1
        
    else:
        print('Incorrect value given, please try again')