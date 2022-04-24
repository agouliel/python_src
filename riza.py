# Biblio Analyshs A' Desmhs

from tabulate import tabulate

def f(x):
    return x**2 - 2

a = int(input('Aristero akro: '))
d = int(input('Deksio akro: '))
n = int(input('Arithmos epanalhpsewn: '))

meso = (a+d)/2

#print('a','\t','d','\t','f(meso)','\t','meso')
mylist = []

for j in range(1,n+1):
    meso = (a+d)/2
    #print(a, '\t', d, '\t', f(meso))
    mylist.append([a,d,f(meso)])
    if f(a)>0 and f(meso)>0: a = meso
    if f(a)>0 and f(meso)<=0: d = meso
    if f(a)<=0 and f(meso)>0: d = meso
    if f(a)<=0 and f(meso)<=0: a = meso

meso = (a+d)/2

#print(a, '\t', d, '\t', f(meso), '\t', meso)
mylist.append([a,d,f(meso),meso])

table = tabulate(mylist, headers=['a','d','f(meso)','meso'])
print(table)