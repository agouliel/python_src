'''

NOTE: THIS IS A PROOF OF CONCEPT
NOTE: only looks for items on main volume

1. Extracts macOS's evaluations (via the ExecPolicy database)
2. Processes evaluations, looking for possibly malicious items

More details: https://objective-see.com/blog/blog_0x64.html#detections

'''

import os
import sqlite3
import platform
import plistlib
import subprocess
import Foundation

#execute sql query 
# via: https://realpython.com/python-sql-libraries/
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as err:
    	exit("(SQL)ERROR: %s" % err) 

# total (possibly malicious) items
count = 0    		

#check 
# < 10.15, not vulnerable
release = platform.mac_ver()[0]
if release[:5] != "10.15" and release[:5] != "10.16":
	exit("ERROR: %s is an unsupported OS (and not vulnerable)" % release) 	

#check
# gotta be root to read the 'ExecPolicy' db
if 0 != os.geteuid():
    exit("ERROR: script must be run with root (to read macOS's 'ExecPolicy' database)") 	

#get (main) volume's inode
# need this to look up file via inode
volInode = os.stat('/').st_dev
print("volume inode: %d" % volInode)

#get Data volume's UUID
# need this, as this is what's stored in the ExecPolicy database
volUUID = subprocess.check_output('diskutil info /System/Volumes/Data | grep "Volume UUID:" | grep -o \'[0-9A-Z]*-[0-9A-Z]*-[0-9A-Z]*-[0-9A-Z]*-[0-9A-Z]*\'', shell=True).strip()
print("volume uuid:  %s" % volUUID)

#open ExecPolicy database
try:
	connection = sqlite3.connect("/private/var/db/SystemPolicyConfiguration/ExecPolicy")
	print("\nopened 'ExecPolicy' database")
    
except sqlite3.Error as err:
	exit("(SQL)ERROR: %s" % err) 	

#query db
items = execute_read_query(connection, "SELECT * FROM policy_scan_cache WHERE volume_uuid = '" + volUUID + "' AND flags = 512 AND bundle_id = 'NOT_A_BUNDLE'")
print("extracted %d evaluated items\n" % len(items))

#scan/parse all items
# looking for file on main volume that
# a) is an app bundle
# b) is a script-based app bundle
# c) is a script-based app bundle, without an Info.plist file
for item in items:
	
	#get file path from vol & file inode
	fileURL = Foundation.NSURL.fileURLWithPath_('/.vol/' + str(volInode) + '/' + str(item[2]))
	result, file, error = fileURL.getResourceValue_forKey_error_(None, "NSURLCanonicalPathKey", None)
	if not result:
		continue

	#check
	# has to be an app bundle
	index = file.find('.app/Contents/MacOS/')
	if(-1 == index):
		#print("not an app, so ignoring")
		continue

	#check 
	# executable file can't be a mach-O 
	fileType = subprocess.check_output(['/usr/bin/file', file])
	if(-1 != fileType.find('Mach-O')):
		#print("is a Mach-O, so ignoring")
		continue
	
	#grab app name
	appName = file[file[:index].rfind('/')+1:index]
	
	#grab file name
	fileName = os.path.split(file)[1]

	#check
	# app name must match file name
	if appName != fileName:
		#print("app name (%s), doesn't match file name (%s)" % (appName, fileName))
		continue

	#check
	# most not have an Info.plist 
	infoPlist = file[:file.find('MacOS/')] + 'Info.plist'
	if os.path.exists(infoPlist):
		#print("app contains Info.plist, so ignoring")
		continue
	
	count +=1
	print("possible malicious application: %s" % file)

print("\ndetected %d possible malicious applications" % count)

       