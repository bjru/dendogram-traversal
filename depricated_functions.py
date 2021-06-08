from PIL import Image, ImageOps, ImageChops
import numpy as np
import numpy.ma as ma
from math import sin,cos,pi

on,off = 1,0


# ===============================================
# Convert Binary list to a decimal number
def binToDec(L):
    number = 0
    for e in L:
        number = e | (number << 1)
    return number

# print("a is 8simple: ",is8SimpleTrueFunction(a))
# print("number is : ",number)


# =====================================================================

# Findes if the set of 8-neghboring pixels is an 8-simple, by collecting neighbors in order:
#  1  2  3
#  8  x  4
#  7  6  5
# #
# #To create list of 8 simples, use this
# List = []
# for i in range(256):
#     binNumber = [int(x) for x in list('{0:08b}'.format(i))]
#     # print()
#     # print(i)
#     if is8SimpleTrueFunction(binNumber):
#         List.append(i)
#         # print()
# #
# print(List)
# Running function on binary lists of size 8 for 0 to 255 yields these as 8-simple:
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 48, 52, 53, 54, 55, 56, 60, 61,
#  62, 63, 64, 65, 67, 69, 71, 77, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 99, 101, 103, 109,
#  111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 131, 133, 135, 141, 143, 149, 151,
#  157, 159, 181, 183, 189, 191, 192, 193, 195, 197, 199, 205, 207, 208, 209, 211, 212, 213, 214, 215, 216, 217, 219, 220,
#  221, 222, 223, 224, 225, 227, 229, 231, 237, 239, 240, 241, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253, 254, 255]


# Funkar ej se false positive below
def is8SimpleTrueFunction(neighborColors):
    eight_simple = []
    for j, e in enumerate(neighborColors):
        # Corners have worse connectivity than neighboring edges:
        # Corner j = 0 has j in [7,0,1] while edge j=1 has j in  [7,0,1,2,3]
        if not (j % 2 == 0 and e == off) and (len(eight_simple) == 0 or e != eight_simple[-1]):
            # If (not background corner) and ()
            # If NOT (Corner AND white) AND (previous pixel different from current pixel)
            # Adds edge pixels and black corner pixels while preventing repetition of same color in list (edge connected to 4 while corner only 2 pixels)
            eight_simple.append(e)
    l = len(eight_simple)
    if l <= 2 or l == 3 and (eight_simple[0] == off or
                             eight_simple[0] == eight_simple[-1]):
        return True
    return False

# Final results!!!!!
# ListIs8simp=  {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 48, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 67, 69, 71, 77, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 99, 101, 103, 109, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 131, 133, 135, 141, 143, 149, 151, 157, 159, 181, 183, 189, 191, 192, 193, 195, 197, 199, 205, 207, 208, 209, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 227, 229, 231, 237, 239, 240, 241, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253, 254, 255}
# ListNot8simp=  {9, 10, 11, 17, 18, 19, 25, 26, 27, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 57, 58, 59, 66, 68, 70, 72, 73, 74, 75, 76, 78, 82, 90, 98, 100, 102, 104, 105, 106, 107, 108, 110, 114, 122, 130, 132, 134, 136, 137, 138, 139, 140, 142, 144, 145, 146, 147, 148, 150, 152, 153, 154, 155, 156, 158, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 182, 184, 185, 186, 187, 188, 190, 194, 196, 198, 200, 201, 202, 203, 204, 206, 210, 218, 226, 228, 230, 232, 233, 234, 235, 236, 238, 242, 250}



def check8simpleList(ListIs8simp,ListNot8simp):
    for i in range(256):
        # if i in ListNot8simp:
        if i in ListIs8simp:
            b = [int(x) for x in list('{0:08b}'.format(i))]
            print(i)
            print("8-simple")
            # print("NOT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!:  8-simple")

            print(b[0], b[1], b[2])
            print(b[7], " ", b[3])
            print(b[6], b[5], b[4])
            answer = input("OK?: ").lower()
            print()
            if answer == "" or answer == "y":
                # ListIs8simp.discard(i)
                ListNot8simp.discard(i)
                print("Discarded")

            elif answer == "n":
                # ListNot8simp.discard(i)
                # ListIs8simp.add(i)

                ListIs8simp.discard(i)
                ListNot8simp.add(i)
                print("Removal done")
            print()
            print()
    print("ListIs8simp= ",ListIs8simp)
    print("ListNot8simp= ",ListNot8simp)
    return ListIs8simp, ListNot8simp

# Rate Neighborhoods as 8-simple or not, adding them to corresponding list
def createSetOf8simple():
    ListIs8simp = set()
    ListNot8simp = set()
    for i in range(256):
        binNumber = [int(x) for x in list('{0:08b}'.format(i))]

        is8Simp = None

        for _ in range(4):
            binNumber.append(binNumber.pop(0))
            binNumber.append(binNumber.pop(0))
            if binToDec(binNumber) in ListIs8simp:
                is8Simp = True
            elif binToDec(binNumber) in ListNot8simp:
                is8Simp = False
        if is8Simp == True:
            for _ in range(8):
                x = binToDec(binNumber)
                ListIs8simp.add(x)
                binNumber.append(binNumber.pop(0))
            continue
        elif is8Simp == False:
            for _ in range(8):
                ListNot8simp.add(binToDec(binNumber))
                binNumber.append(binNumber.pop(0))
            continue
        print()
        print(i)
        # if is8SimpleTrueFunction(binNumber):
        b = binNumber
        print(b[0],b[1],b[2])
        print(b[7]," ",b[3])
        print(b[6],b[5],b[4])
        while True:
            answer = input("Is 8-simple?").lower()
            # answer = ''
            if answer == "":
                ListIs8simp.add(i)
                break
            elif answer == "z":
                ListNot8simp.add(i)
                break
            else:
                print("('' for Yes) or (z for No)")
        print("Is 8-simple: ",ListIs8simp)
        print("Not 8-simple: ",ListNot8simp)
#

eightSimpSet = set()
for i in range(256):
    binNumber = [int(x) for x in list('{0:08b}'.format(i))]
    # print()
    # print(i)
    if is8SimpleTrueFunction(binNumber):
        eightSimpSet.add(i)
        # print()
#
print(eightSimpSet)

# binNumber = [int(x) for x in list('{0:08b}'.format(56))]
# for i in range(8):
#     a = binNumber.append(binNumber.pop(0))


#todo använd input 1,0 för att avgöra detta
# False positive
# 245, 241, 237,231,229,227,225





# ===============================================
# Create image with X, Y or I shape
def createCross(dim,shape,name):
    A = np.ones((dim,dim))*255
    # Create Cross
    if shape == "X":
        A[0:,round((dim-1)/2)]=0
        A[round((dim-1)/2),0:]=0
    elif shape == "Y":
        A[0:round((dim-1)/2),round((dim-1)/2)]=0
        A[round((dim-1)/2),0:]=0
    elif shape == "I":
        A[0:,round((dim-1)/2)]=0
    print(A)
    print("\n\n")
    im = Image.fromarray(A).convert("L")
    # im.show()
    name = "graphs/"+name+".png"
    print(name)
    im.save(name, "PNG")




if __name__ == "__main__":
    # createCross(5,"I","crossI4")
    dim =100
    A = np.ones((dim, dim)) * 150
    im = Image.fromarray(A)

    # im.show()