from modules import safeconvert
from modules import makeplaylist
import sys
import os

###Gets CSV File from Arguments
try:
    csvin = sys.argv[1]
except:
    csvin = input("Please give the absolute path to your CSV File: \n")

###Defines Delimiter
delim = input('Please Define Your Path Delimiter: \n')

###Defines Path Prefix
path_prefix = input("Do you want to insert path for iTunes to read? Leave blank for absolute path \n")

if path_prefix == '':
    path_prefix = 0
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

makeplaylist(csvin, delim, path_prefix, dir, playlistname)