# Python - Eisagwgh stous Ypologistes
import threading
import time as tm
import os

def playsound():
    while True:
        os.system('say "Beer time."') # https://stackoverflow.com/questions/42150309/how-to-make-a-sound-in-osx-using-python-3
        tm.sleep(0.1)

def countup():
    for i in range(20):
        print(i, end='\r')
        tm.sleep(0.5)

threading.Thread(target=playsound).start() # how to stop it?
threading.Thread(target=countup).start()