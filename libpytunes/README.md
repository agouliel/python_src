https://github.com/liamks/libpytunes

from libpytunes import Library

l = Library("/Users/agou/Music/Library.xml")

for id, song in l.songs.items():
    if song and song.rating:
        if song.rating > 80:
            print(song.name, song.rating)

https://stackoverflow.com/questions/52176570/deprecationwarning-with-readplist-attributeerror

pl=plistlib.readPlist(fileName)

replace the line containing readPlist with

with open(fileName, 'rb') as f:
    pl = plistlib.load(f)
