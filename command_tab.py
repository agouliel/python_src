#!/usr/bin/env python3

# https://discussions.apple.com/thread/3690632
# https://gist.github.com/nzaillian/622181
# tab code 48
# https://stackoverflow.com/questions/9522324/running-python-in-background-on-os-x

# the below uses AppleScript, which is Mac-only
# a cross-platform version can be found in pyautoguitest/alt_tab.py (uses pyautogui)

import os, time, random

cmd_start = """osascript -e 'tell application "System Events"
key down command
"""
cmd_end = """key up command
end tell'"""

while True:
    cmd_current = cmd_start

    # add random number of tab presses
    number_of_tabs = random.randint(1,6)
    for i in range(1, number_of_tabs):
        cmd_current += 'keystroke tab\n'

    cmd_current += cmd_end
    #print(cmd_current)
    os.system(cmd_current)

    # sleep for a random duration between 1 and 3 minutes
    number_of_seconds = random.randint(60, 180)
    time.sleep(number_of_seconds)
