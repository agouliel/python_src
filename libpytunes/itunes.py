# https://github.com/liamks/libpytunes

# https://stackoverflow.com/questions/52176570/deprecationwarning-with-readplist-attributeerror
# pl = plistlib.readPlist(fileName)
# replace the line containing readPlist with
# with open(fileName, 'rb') as f:
#   pl = plistlib.load(f)

import Library as lib

l = lib.Library("/Users/agou/Music/Library.xml")

for id, song in l.songs.items():
    if song.comments:
        print(str(id) + ';' + song.name + ';' + song.artist + ';' + song.comments.replace('\n', ' ').replace('"',''))
    else:
        print(str(id) + ';' + song.name + ';' + song.artist + ';')
        