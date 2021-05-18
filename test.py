import numpy as np
import numpy.ma as ma

on=1
off=0

x = np.array([1,1,1,0,0])
mx = ma.masked_array(x, mask=[0, 0, 1, 1, 0])

test = np.nonzero(mx)
# print(test)

w,h = 10,10
# todo Använd detta för att skapa masken
a = np.ones((w,h))
print(a)
print()
a[1:w-1,1:h-1] = 0  #sista i :y räknas ej => [x,x+1,....y-1]
# a[y,x]
print(a)

newBBox = ((3,8), (1,9))
# Använd detta för att uppdatera masken
# a[0:3,0:2] = 1
# eller a=1 och ny a[...] = 0

