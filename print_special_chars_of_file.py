with open('file.txt','r') as f:
  data = f.read()

for c in data:
  print(ord(c), hex(ord(c)), repr(c), c.encode('utf-8'))
