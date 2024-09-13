# Exportify Downloader
### Quick and dirty spotify playlist downloader - v 0.1 (Alpha)

## **Installation Instructions**

This may come as a suprise to you, but you'll need Python installed.
### Additionally, you'll need:
 - From Pip:
   - Pytube
   - EyeD3
 - Installed Separately:
   - [FFmpeg](https://ffmpeg.org/)

## **How to Use**

If you're looking to download one file, select option 2 in the inital questions and follow the prompts.

For CSV playlist downloading:

Using [exportify.net](https://exportify.net/), grab the playlist you want and download it.

Run main.py either on it's own, or with the CSV file as an argument

    e.g: python -e main.py /the/absolute/path/of/csv.csv

Exportify downloader will then ask you a bunch of questions about how you want the files processed.

It's a bodge, but it works

## **Technical Breakdown**
Alrighty, this code sucks. It is by no means a work of art (I'm a Photographer/Video editor, not a software engineer) but fuck it, it works.

### CSV Parser
There's probably an easier way to do this, but for each line in the CSV I create a new entry in separate lists just so I have an easy way to query against it.

Each option uses different data, but the common ones are "Track Name" & "Artist Name"

### General Downloady Shit
Using pytube, the script will query youtube for the song & artist's names, followed by "Topic"

Usually, YouTube Music will auto populate their stuff into channels ending in topic - adding that makes it a bit more reliable

Initially, I had this written to query the search URL and, using some regexes I didn't actually write, grabbing the first ID it sees but *thankyou, oh lord of advertising Alphabet Inc* it started returning the results as ads. Which is bullshit. I don't want a Jeep ad on my iPod.

SO I then read the pytube documentation to try and figure out if it would return anything for unlisted videos (which they usually are) and I realised it had a search function all  along. Implemented that into the search function I had, and we're golden. There is definintely a more efficient way to do this but I need this working ASAP so I can download a bunch of shit for work tomorrow.

Then, with the video ID, downloads that and *badabing badaboom* you've got yourself something that searches and downloads YouTube. I am a gigagenius.

Then FFmpeg converts it to an mp3 and you're golden.

### DJ Playlist Maker
There are two ways this script is designed for, let's start with the one I wrote 10mins ago (at time of writing) so I don't have to re-decipher my code.

TL;DR this option will download the files and name them in the following format:

    [key_tempo_genre]artist-track.mp3


The key is encoded into Camelot Codes for easy mixing.

This doesn't output any files, just outputs a folder full of stuff in the ~/playlists directory

### iTunes Playlist Maker
I built this one as an easy way to grab my Spotify playlists and chuck them on my iPod

This portion of the script will take the output files from the ytquery/ytdown functions and write the details into a tab-separated-values (TSV) .txt file because that's how iTunes reads this shit, idk ask Apple.

The csv parser that's inbuilt to Python can just deal with different delimiters, which makes my life so much easier

The format & variables written is as follows:

| Name | Artist | Composer | Album | Grouping | Work | Movement Number | Movement Count | Movement Name | Genre | Size | Time | Disc Number | Disc Count | Track Number | Track Count | Year | Date Modified | Date Added | Bit Rate | Sample Rate | Volume Adjustment | Kind | Equaliser | Comments | Plays | Last Played | Skips | Last Skipped | My Rating | Location |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **trname** | **arname** | *blank* | **alname** | *blank* | *blank* | *blank* | *blank* | *blank* | *blank* | **size** | **dur** | *blank* | *blank* | **trnum** | *blank* | *blank* | **dateadd** | **dateadd** | **bitrate** | **samplerate** | *blank* | **kind** | *blank* | *blank* | *blank* | *blank* | *blank* | *blank* | *blank* | **path** |

As you can see, the majority of the values within that table can be left blank. Additionally, from what I can tell, the plugin I'm using for writing id3 data currently doesn't support adding release year/genres so they're being written straight into the playlist file and iTunes just does it's thing... fkn sick