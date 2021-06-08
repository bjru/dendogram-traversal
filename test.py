import numpy as np
import numpy.ma as ma
from PIL import Image, ImageOps
#
# on=1
# off=0
#
# x = np.array([1,1,1,0,0])
# mx = ma.masked_array(x, mask=[0, 0, 1, 1, 0])
#
# test = np.nonzero(mx)
# # print(test)
# # mask på alla 0:or
# w,h = 3,3
# # todo Använd detta för att skapa masken
# a = np.ones((w,h))
# print(a)
# print()
# a[1:3,1] = 0  #sista i :y räknas ej => [x,x+1,....y-1]
# # a[y,x]
# print(a)
#


# mx = ma.masked_array(np.ones((w,h)), mask=a)
# print()
# print(mx)
# newMask = np.zeros((3,3))
# # newMask[2,1] = 1
# mx = ma.masked_array(mx, mask=newMask)
# mx[2,1] = ma.masked
# # test = np.nonzero(mx)
# print()
# print(mx)
# # (Y_array, X_array)
#
# # # print(test)
# # newBBox = ((3,8), (1,9))
# # # Använd detta för att uppdatera masken
# # # a[0:3,0:2] = 1
# # # eller a=1 och ny a[...] = 0
# # w,h = 5,10
# # mask = np.ones((h,w))
# # mask[1:h-1, 1:w-1] = 0
# # print()
# # print(mask)


# x = np.ones((3,3))
# mx = ma.masked_array(x,mask=np.ones((3,3)))
# print(x)
# print()
# print(mx)
# print()
#
# # mx[1,1] = 3
# mx[1,1] = ma.nomask
# print(x)
# print(mx)

