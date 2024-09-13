from modules import safeconvert
from modules import makeplaylist
from modules import makeDJPlaylist
from modules import pureDownload
from modules import ytdown
import sys
import os

brk = 0

while brk != 1:
    version = input("Please select use case: \n 1: Bulk downloading from CSV\n 2: Single ID download\n")
    version = int(version)

    ### Bulk CSV Download
    if version == 1:
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

        ###Defines Use Case (see readme for breakdown)
        while brk != 1:
            usage = input("Please select use case: \n 1: Porting Spotify Playlist to iTunes \n 2: Downloading tracks to mix\n 3: Pure CSV Download\n")
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

        brk = 1

    ### Single ID Download
    if version == 2:
        ID = input("What video would you like to download? Input either the full URL or just the ID \n")
        # Checks if full URL
        if "youtu.be" in ID:
	        # If it contains http:// or https://, split by the / & get the appropriate section
            if "https://" in ID or "http://" in ID:
                ID = str(ID.split("/")[3])[0:11]
            else:
                ID = str(ID.split("/")[1])[0:11]
        elif "youtube.com" in ID:
            # Find the 10 characters after v= in the string
            v = ID.find("v=")+2
            ID = ID[v:v+11]
        
        filename = input("Please define your file name (without extension): \n")
        folder = input("Where would you like the file downloaded (Absolute path please): \n")
        delim = input('Please Define Your Path Delimiter: \n')

        ytdown(ID, folder, delim, filename)

        brk = 1