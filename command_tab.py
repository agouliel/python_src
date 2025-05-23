# https://discussions.apple.com/thread/3690632
# https://gist.github.com/nzaillian/622181
# tab code 48

import os, time, random

cmd_start = """osascript -e 'tell application "System Events"
key down command
"""
cmd_end = """key up command
end tell'"""

while True:
    number_of_tabs = random.randint(1,6)
    cmd_current = cmd_start
    for i in range(1, number_of_tabs):
        cmd_current += 'keystroke tab\n'
    cmd_current += cmd_end
    #print(cmd_current)
    os.system(cmd_current)
    number_of_seconds = random.randint(200, 500)
    time.sleep(number_of_seconds)

