f = input('Input the function: y = ')
l1 = input('Input the first limit: ')
lim1 = eval(l1)
l2 = input('Input the second limit: ')
lim2 = eval(l2)
s = input('Input the step: ')
st = eval(s)

i = 0
x = lim1

while x <= lim2:
  y = eval(f)
  i = i + st*y
  x = x + st

print('The integral is:', i)
