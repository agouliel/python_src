def paragontiko(n):
    print('call with parameter:', n)
    if n==1:
        print('return 1')
        return 1
    else:
        apot = n * paragontiko(n-1)
        print('μεχρι τωρα', n, '*(', n-1, ')! =', apot)
        return apot

print(paragontiko(5))
