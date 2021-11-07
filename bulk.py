from modules import makeplaylist
import os

folder = input("Input Folder: \n")
foldercontents = os.listdir(folder)
path = os.path.abspath(folder)
delim = input('Please Define Your Path Delimiter: \n')
path_prefix = input("Do you want to insert path for iTunes to read? Leave blank for absolute path \n")

try:
    os.mkdir(os.path.expanduser('~') + delim + 'playlists')
except:
    print ('Playlists folder exists')

for csv in foldercontents:
    tmp = csv.split('.')
    playlistname = tmp[0]
    print ("#################################################################################### Generating " + playlistname + '...')
    try:
        dir = os.path.expanduser('~') + delim + 'playlists' + delim + playlistname
        os.mkdir(dir)
    except:
        print ("Folder already exists...")
    csvin = path + delim +csv
    makeplaylist(csvin, delim, path_prefix, dir, playlistname)