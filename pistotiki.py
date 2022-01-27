import sys

for numstr in sys.argv[1]:
  try:
    i = int(numstr)
    if i == 0:
      print('9', end='')
    else:
      print(int(i)-1, end='')
  except:
    print(numstr, end='')

print()
