# normal calculation
def fibe(n):
    a,b = 1,1
    while a<=n:
        global x
        x+=1
        #print(a, end=' ')
        a,b = b,a+b
    return a

# recursive
def fiba(n):
   if n in (1,2):
     return 1
   else:
     global i
     i+=1
     return fiba(n-1) + fiba(n-2)

# recursive with dictionary
f={1:1, 2:1}

def fibd(n):
    if not n in f:
        global j
        j+=1
        f[n] = fibd(n-1) + fibd(n-2)
    return f[n]

# recursive with list (not working)
mylist = [1, 1]

def fibl(n):
    curr = fibl(n-1) + fibl(n-2)
    if mylist.count(curr) == 0:
        global k
        k+=1
        mylist.append(curr)
    return mylist[-1]

# test the functions
x=i=j=k=0
print(fibe(14930351))
print(x)
print(fiba(36))
print(i)
print(fibd(36))
print(j)
#print(fibl(36)) # not working
#print(k)
