# https://twitter.com/mathsppblog/status/1453771872051531784

import signal

_ = signal.signal(signal.SIGINT, lambda *_: print("no"))
while True:
  pass
