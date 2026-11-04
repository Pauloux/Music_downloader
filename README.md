# About

The **music downloader** project aims at managing an offline playlist downloaded
from YouTube.

## What is the problem with regular YouTube playlists?

If a song is removed from YouTube, then you lose the information of what song
it was. If you have hundreds or thousands of songs in your playlist, you cannot
remember which song it was, and you simply lost a song if you need to download
it again.

## How does this project solve this issue?

This project stores information about songs in a local database file (CSV
format). If a song is removed from YouTube, you can still see which song it was
(title, artist and album). You can then simply update the YouTube URL of this
database entry, and continue enjoying your music forever !

## Other features

This project also includes these features:
- naming downloaded files to the following format: "Artist - Title", thus
helping to stay organized and allowing you to find songs more easily.
- Applying metadata (title, artist and album) so music apps (smartphones, cars,
etc.) can display them correctly. This also helps to sort your songs.
- Applying a gain (non-destructive, it is just a gain saved as a metadata) to
normalize the sound intensity. This allows you to listen to your music without
changing the volume between each song because they are not recorded with the
same default volume.

# Dependencies

/!\ This project is made for Linux, and more specifically for Ubuntu. Some 
adjustments may be necessary to use it on other platforms /!\

- yt-dlp (to download songs from YouTube): <https://github.com/yt-dlp/yt-dlp>.
- id3v2 (to apply metadata): <https://sourceforge.net/projects/id3v2/>.
- mp3gain (to normalize the sound intensity for all songs):
<https://mp3gain.sourceforge.net/index.php>.

Links in French for Ubuntu:
- yt-dlp: <https://doc.ubuntu-fr.org/yt-dlp> (Follow the "Binaire isolé"
section to be able to keep yt-dlp up to date because YouTube regularly breaks
it).
- id3v2: <https://doc.ubuntu-fr.org/id3v2>
- mp3gain: <https://doc.ubuntu-fr.org/mp3gain>

# How to use the program?

## Create the database

The database is a CSV (Comma-Separated Values) file:
- The first row contains the name of the columns: `url;artist;title;album`.
- Then, on each row, you can add a song by typing *in the exact same order* as
the column row the data associated with the song. An example is available in the
`music_info.csv` file or below.
- To keep your database clean, you can have blank lines or comments. A comment
is a row containing the character `#` in its first column.

### Database example
```
url;artist;title;album
# A
https://www.youtube.com/watch?v=rVeMiVU77wo;Alt-J;Breezeblocks;An awesome wave
https://www.youtube.com/watch?v=PqTMyOllv4A;Avicii;Hey brother;True
# C
https://www.youtube.com/watch?v=KdOD0fZs_XU;C418;Mice on Venus;Minecraft
# D
https://www.youtube.com/watch?v=TnQsZPk93FA;Daft Punk & Pharrell Williams & Nile Rodgers;Get Lucky;Random access memories
https://www.youtube.com/watch?v=RM4TfzprAwg;David Guetta & Sam Martin;Lovers on the sun;Listen
```

## Download the songs

Run the file `music_downloader.py` with Python.

Once the program finished running, a short report is available in the console.
This report lists all the downloads that have failed if there are any. Thus, you
can retry the download, or verify if the url is still available on YouTube (and 
correct your database if not). A log file (`music_downloader.log` by default) is
also created if you need to investigate further when errors occur.

Please note that songs already in the output directory (music by default) are
**not** downloaded again to save time and energy. If you want to download again
a song, simply delete it from the output directory and re-run the program.

## Advanced usage

- One can modify the output directory and CSV file used by modifying the
corresponding variable at the beginning of the Python program. File format can
also be changed (mp3 by default), and the CSV separator can be changed as well.

# There is a bug, what do I do?

This is a tool I made for myself. I try to make it work as best as possible for
me, and there is no guarantee it will work for you.

You are free to use and modify the tool as much as you want. Contributions are
welcome if you want to improve the program !
