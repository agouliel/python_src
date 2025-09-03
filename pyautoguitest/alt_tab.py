import os, time, random, pyautogui

modifier_key = 'command' if os.name == 'posix' else 'alt' # windows --> 'nt'


while True:
    pyautogui.keyDown(modifier_key)

    # add random number of tab presses
    number_of_tabs = random.randint(1,6)
    for i in range(1, number_of_tabs):
        pyautogui.press('tab')

    pyautogui.keyUp(modifier_key)

    # sleep for a random duration between 1 and 3 minutes
    number_of_seconds = random.randint(60, 180)
    time.sleep(number_of_seconds)
