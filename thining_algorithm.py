from PIL import Image, ImageOps
import numpy as np
import numpy.ma as ma
from math import sin,cos,pi


import cProfile
import pstats

# 1 is part of graph and 0 is background (on monitor, displayed as black background with a white graph and text)
on,off = 1,0

# Set of all 8-simple pixels where numbers in binary represent different positions of 8-neighboring pixels
eightSimpleSet = {0, 1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16, 24, 28, 30, 31, 32, 48, 56, 60, 62, 63, 64, 96, 112, 120, 124,
                  126, 127, 128, 129, 131, 135, 143, 159, 191, 192, 193, 195, 199, 207, 223, 224, 225, 227, 231, 239, 240,
                  241, 243, 247, 248, 249, 251, 252, 253, 254, 255}


def thining(filename):
    """
    # Thining algorithm performed on an image with filepath given as an attribute.
    :param filename: filepath as a string to an image
    :return: an image object
    """


    # Threshold for making image binary (as every pixel is between 0 and 255)
    threshold = 200
    def threshold_function(x):
        """
        # Inverts image white to black
        :param x: a pixel value
        :return: new pixel value
        """
        return off if x > threshold else on
    # Makes image binary
    im = Image.open(filename).convert("L").point(threshold_function, mode='1')
    # Crop with bounding box crops largest possible black border around image
    im = im.crop(im.getbbox())
    # adds a 1 pixel wide border around image to prevent algorithm from trying to access pixels outside
    im = ImageOps.expand(im, border=1, fill=off)

    # Used to acces pixel data
    px = im.load()
    # Converts image into a Numpy array, then creates a mask of the Numpy array, used to mask away background pixels and
    # pixels which should not be removed
    maskArray = ma.masked_equal(np.asarray(im), off)

    pixel_deleted = True
    passCount = 0
    while pixel_deleted:

        passCount += 1
        pixel_deleted = False
        for v in range(4):
            # Results in 4 iterations with values  (1, 0), (1, 0), (-1, 0), (0, -1) : E, N, W, S
            d = (round(cos(v * pi / 2)), round(sin(v * pi / 2)))

            # Pixels to remove in this sub-pass
            marked_pixels = []
            # All non-background pixels
            nonzero = np.nonzero(maskArray)

            # For each pixel (y,x)
            for (y, x) in zip(nonzero[0], nonzero[1]):
                # A) can be skipped as we use maskArray[y,x] = off in curried function rmM()
                # A) Pixel is off
                if px[(x, y)] == off:
                    maskArray[y,x] = ma.masked
                    continue

                # B) Pixel is on, but not edge in direction d
                if px[(x + d[0], y + d[1])] == on:
                    continue
                # C) Pixel is an endpoint
                # List of colors of neighbor pixels, start in top-left pixel, goes around clockwise and end in left pixel
                neighborColors = [px[(x - 1, y - 1)], px[(x, y - 1)], px[(x + 1, y - 1)],
                                  px[(x + 1, y)], px[(x + 1, y + 1)], px[(x, y + 1)], px[(x - 1, y + 1)], px[(x - 1, y)]]
                if neighborColors.count(on) <= 1:
                    maskArray[y,x] = ma.masked
                    continue
                # D) Is not 8-Simple, removing pixel does affect connectivness of neighboring pixels, therefore don't remove pixel
                if not is8Simple(neighborColors):
                    maskArray[y,x] = ma.masked
                    continue

                # mark pixel i_xy for deletion
                marked_pixels.append((x,y))
                pixel_deleted = True
            # Removes marked pixels using a curried function
            list(map(removeMarked(px, maskArray), marked_pixels))

    print("Passes: ", passCount)
    # masked enries in maskArray are lost. therefore Image.fromarray(maskArray) is not a good method to access neighboring pixel-data
    return im

def removeMarked(px, maskArray):
    """
    Currying function that lets you remove pixels based on index, used in a map-function
    :param px: array of pixels
    :return: a curried function that removes pixels based on index.
    """
    def rmM(i_xy):
        x,y = i_xy
        # Lets us skip A) in thinning()
        maskArray[y,x] = off
        px[i_xy] = off
    return rmM

def is8Simple(neighborColors):
    """
    Finds out if array of size 8 is an 8-simple
    :param neighborColors:
    :return: True if it is an 8-simple, false otherwise
    """
    number = 0
    for e in neighborColors:
        number = e | (number << 1)
    return number in eightSimpleSet




if __name__ == "__main__":
    pr = cProfile.Profile()
    filename = "graphs/lars_graph16.png"
    # filename = "graphs/post_thining1.png"
    # im.show()
    pr.enable()

    im = thining(filename)

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(15)
    # im.show()
