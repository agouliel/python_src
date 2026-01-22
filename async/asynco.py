# https://www.youtube.com/watch?v=Y4Gt3Xjd7G8
# Build Your Own Async - David Beazley - PyCon India, Chennai, October 14, 2019

import time
from collections import deque

class Scheduler:
  def __init__(self):
    self.ready = deque() # Functions ready to execute
  
  def call_soon(self, func):
    self.ready.append(func)

  def run(self):
    while self.ready:
      func = self.ready.popleft()
      func()

#----------------------------------------------------
# Alternative version, to manage time (instead of sleep)
#----------------------------------------------------
"""
  def call_later(self, delay, func):
    deadline = time.time() + delay     # Expiration time
    self.sleeping.append((deadline, func))
    self.sleeping.sort()      # Sort by closest deadline (or use heapq)

  def run(self):
    while self.ready or self.sleeping:
      if not self.ready:
        # Find the nearest deadline
        deadline, func = self.sleeping.pop(0)
        delta = deadline - time.time()
        if delta > 0:
          time.sleep(delta)
        self.ready.append(func)

      while self.ready:
        func = self.ready.popleft()
        func()
"""
#----------------------------------------------------

sched = Scheduler() # Behind scenes scheduler object

#----------------------------------------------------

# functions can't loop
# each one schedules its next iteration

def countdown(n):
  if n > 0:
    print('Down', n)
    time.sleep(1)
    sched.call_soon(lambda: countdown(n-1))

def countup(stop, x=0):
  if x < stop:
    print('Up', x)
    time.sleep(1)
    sched.call_soon(lambda: countup(stop, x+1))

#----------------------------------------------------

sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(5))
sched.run()