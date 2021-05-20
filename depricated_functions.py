
on,off = 1,0

# Findes if the set of 8-neghboring pixels is an 8-simple, by collecting neighbors in order:
#  1  2  3
#  8  x  4
#  7  6  5
#
# Running function on binary lists of size 8 for 0 to 255 yields these as 8-simple:
# {0, 1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16, 24, 28, 30, 31, 32, 48, 56, 60, 62, 63, 64, 96, 112, 120, 124,
#                   126, 127, 128, 129, 131, 135, 143, 159, 191, 192, 193, 195, 199, 207, 223, 224, 225, 227, 231, 239, 240,
#                   241, 243, 247, 248, 249, 251, 252, 253, 254, 255}

def is8SimpleTrueFunction(neighborColors):
    eight_simple = []
    for j, e in enumerate(neighborColors):
        if not (j % 2 == 0 and e == off) and (len(eight_simple) == 0 or e != eight_simple[-1]):
            # If NOT (Corner AND white) AND (previous pixel different from current pixel)
            # Adds edge pixels and black corner pixels while preventing repetition of same color in list (edge connected to 4 while corner only 2 pixels)
            eight_simple.append(e)
    l = len(eight_simple)
    if l <= 2 or l == 3 and (eight_simple[0] == off or
                             eight_simple[0] == eight_simple[-1]):
        return True
    return False

