
from PIL import Image, ImageOps
import numpy as np
import numpy.ma as ma
from math import sin,cos,pi

on,off = 255,0

def threshold_function(x):
    """
    # Inverts image white to black
    :param x: a pixel value
    :return: new pixel value
    """

    # print(x)
    if x == 0: return 0
    elif x == 255: return 100
    else: return x
    # return lambda x: off if x == on else on if x == off else x




im = Image.open("graphs/lars_graph16_post_run.png")
# im.show()
# im_invert = ImageOps.invert(im)
# im_invert = Image.eval(im, threshold_function())
# im = im.point(threshold_function)

# a = np.array([[[0,0,0],[255,255,255]],[[2,2,2],[1,2,2]],[[3,2,4],[6,2,5]]])
# print (np.where(a == [0,0], [7,7], a)
# )

# for x in y for y in a:
im.show()
a = np.array(im)
for x in a:
    for y in x:
        if np.all(y == 0): y[y==0]=255
        elif np.all(y == 255): y[y==255]=0
print (a)

im =Image.fromarray(a)
im.show()



# {(255, 73, 73), (0, 0, 0), (255, 255, 255)}
# im_invert.show()
# im = im.point(range(256, 0, -1) * 3)


