from PIL import Image, ImageOps
import numpy as np
import numpy.ma as ma
from math import sin,cos,pi

# import cProfile
# import pstats

# 1 is part of graph and 0 is background (on monitor, displayed as black background with a white graph and text)
on,off = 1,0

# Set of all 8-simple pixels where numbers in binary represent different positions of 8-neighboring pixels,
# note that for binary representation, top left neighbor pixel is the left most bit and left neighbor pixel is the right most bit in an 8-bit number
# ListNot8simp=  {9, 10, 11, 17, 18, 19, 25, 26, 27, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 49, 50, 51, 57, 58, 59, 66, 68, 70, 72, 73, 74, 75, 76, 78, 82, 90, 98, 100, 102, 104, 105, 106, 107, 108, 110, 114, 122, 130, 132, 134, 136, 137, 138, 139, 140, 142, 144, 145, 146, 147, 148, 150, 152, 153, 154, 155, 156, 158, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 182, 184, 185, 186, 187, 188, 190, 194, 196, 198, 200, 201, 202, 203, 204, 206, 210, 218, 226, 228, 230, 232, 233, 234, 235, 236, 238, 242, 250}
# ListIs8simp=  {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 48, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 67, 69, 71, 77, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 99, 101, 103, 109, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 131, 133, 135, 141, 143, 149, 151, 157, 159, 181, 183, 189, 191, 192, 193, 195, 197, 199, 205, 207, 208, 209, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 227, 229, 231, 237, 239, 240, 241, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253, 254, 255}
eightSimpleSet = {0, 1, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24, 28, 29, 30, 31, 32, 48, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 67, 69, 71, 77, 79, 80, 81, 83, 84, 85, 86, 87, 88, 89, 91, 92, 93, 94, 95, 96, 97, 99, 101, 103, 109, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 131, 133, 135, 141, 143, 149, 151, 157, 159, 181, 183, 189, 191, 192, 193, 195, 197, 199, 205, 207, 208, 209, 211, 212, 213, 214, 215, 216, 217, 219, 220, 221, 222, 223, 224, 225, 227, 229, 231, 237, 239, 240, 241, 243, 244, 245, 246, 247, 248, 249, 251, 252, 253, 254, 255}

def threshold_function(threshold):
    """
    # Inverts image white to black
    :param x: a pixel value
    :return: new pixel value
    """
    return lambda x: off if x > threshold else on

def thining(filename, threshold = 200,viewBeforeThining=False):
    """
    # Thining algorithm performed on an image with filepath given as an attribute.
    :param filename: filepath as a string to an image
    :return: an image object
    """

    # Makes image grayscale
    im = Image.open(filename).convert("L")

    if viewBeforeThining:
        im.show(title="Grayscale, pre-thinning")

    # Makes image binary, threshold is between 0 and 255
    im = im.point(threshold_function(threshold), mode='1')

    if viewBeforeThining:
        im.show(title="Post-binary and -inverted")

    # Crop with bounding box crops largest possible black border around image
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
    return im, Image.open(filename).convert("L")

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
    # filename = "graphs/lars_graph16.png"
    filename = "graphs/lars_graph2.png"
    # filename = "graphs/crossY3.png"
    # filename = "graphs/test2.png"
    # im = Image.open(filename)
    # im.show(title="Pre-thinning")
    pr.enable()

    im, imGray = thining(filename,threshold=200)

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(15)
    im.show(title="Testing thinning")

    name = filename.split(".")
    name = name[0] + "_post_thining." + name[1]
    im.save(name, "PNG")

