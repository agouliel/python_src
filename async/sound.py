# Python - Eisagwgh stous Ypologistes
import multiprocessing as mp
import time as tm
import os

def playsound():
    while True:
        os.system('say "Beer time."') # https://stackoverflow.com/questions/42150309/how-to-make-a-sound-in-osx-using-python-3
        tm.sleep(0.1)

if __name__ == '__main__':
    p = mp.Process(target=playsound)
    p.start()
    for i in range(20):
        print(i, end='\r')
        tm.sleep(0.5)
    p.terminate()
    p.join()
