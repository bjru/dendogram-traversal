from PIL import Image, ImageOps
import numpy as np
from math import sin,cos,pi


import cProfile
import pstats

on = 1
off = (on+1)%2
# on, off = 0,1
# on, off = 1,0
# on, off = 0, 255

# todo maybe remove
# Todo använd Numpys np.nonzero istället
# Returns a list of all pixels with coordinates of given "color", the pixels are collected through listOfPixels and/or bound
# listOfPixels Contains a list of pixel-coordinates that are checked
# bound is a bounding box of the image, only pixels inside the box was changed last iteration
# def colorPixelLocations(px, color=on, listOfPixels=None, bound=None):
#     if listOfPixels is None and bound is not None:
#         # When content in bound is unknown
#         return [(col, row) for col in range(bound[0][0], bound[1][0]) for row in range(bound[0][1], bound[1][1]) if px[(col, row)] == color]
#     elif listOfPixels is not None and bound is None:
#         # When black pixels of last pass, across image is known
#         return [pixel for pixel in listOfPixels if px[pixel] == color]
#     elif listOfPixels is not None and bound is not None:
#         # When black pixels of last pass, across image is known and no changes were made outside bound
#         return [pixel for pixel in listOfPixels if px[pixel] == color and bound[0][0] <= pixel[0] <= bound[1][0] and bound[0][1] <= pixel[1] <= bound[1][1]]
#     else:
#         raise AttributeError("listOfPixels and bound can't both be None")


def thining(filename):
    # on is color of graph and off is color of background
    # on, off = 0,1
    # Threshold for making image binary (as every pixel is between 0 and 255)
    threshold = 200
    # 1 is part of graph and 0 is background (on monitor, displayed as black background with a with graph and text)
    # Inverts image white-black
    def threshold_function(x):
        return off if x > threshold else on
    im = Image.open(filename).convert("L").point(threshold_function, mode='1')
    # Crop with bounding box crops largest possible black border around image
    im = im.crop(im.getbbox())
    # adds a 1 pixel wide border around image to prevent algorithm from trying to access pixels outside
    im = ImageOps.expand(im, border=1, fill=off)

    array = np.asarray(im)

    # todo maybe remove
    width, height = im.size

    # todo maybe remove
    px = im.load()

    # todo maybe remove
    # directions = ["N","S","W","E"]
    # coordinate (0,0) is top-left corner
    # directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # todo maybe remove
    # bounding box of the image, only pixels inside the box was changed last iteration (at initiation it's 1 pixel inside the edge of the image)
    # bounding_box_of_changes = ((1, 1), (width - 1, height - 1))
    bbox = ((1, 1), (width - 1, height - 1))

    # Returns list of pixels that are ON (on=1 and off=0) within bounding_box_of_changes
    # nonzero = np.nonzero(array)
    # ON_pixel_coordinates_within_bound = colorPixelLocations(
    #     px, color=on, listOfPixels=None, bound=bounding_box_of_changes)


    pixel_deleted = True
    index = 0
    while pixel_deleted:
        index += 1
        # todo maybe remove
        # ON_pixel_coordinates_within_bound = colorPixelLocations(
        #     px, color=on, listOfPixels=ON_pixel_coordinates_within_bound, bound=bounding_box_of_changes)
        # Returns list of pixels that are ON (on=1 and off=0) on format (L_Yvalues, L_Xvalues)
        nonzero = np.nonzero(array)
        nonzero_indices = [(x, y) for (y,x) in zip(nonzero[0],nonzero[1])
                           if bbox[0][0] <= x <= bbox[1][0] and bbox[0][1] <= y <= bbox[1][1]]


        # todo maybe remove
        crop_constraint = ((width - 1, height - 1), (1, 1))
        pixel_deleted = False

        # todo mer ineffektivt än listan (directions)?
        # for i, d in enumerate(directions):
        for v in range(4):
            # Results 4 iterations with values  (1, 0), (1, 0), (-1, 0), (0, -1) : E, N, W, S
            d = (round(cos(v * pi / 2)), round(sin(v * pi / 2)))

            # Pixels to remove
            marked_pixels = []

            # For each pixel i_xy
            for (x, y) in nonzero_indices:
                # i_xy = (x, y)
                # # i_d = (x + directions[i][0], y + directions[i][1])
                # i_d = (x + d[0], y + d[1])

                # A) Pixel is off
                if px[(x, y)] == off:
                    continue
                # B) Pixel is on, but not edge in direction d
                if px[(x + d[0], y + d[1])] == on:
                    continue
                # C) Pixel is an endpoint
                # List of colors of neighbor pixels, start in top-left pixel, goes around clockwise and end in left pixel
                neighborColors = [px[(x - 1, y - 1)], px[(x, y - 1)], px[(x + 1, y - 1)],
                                  px[(x + 1, y)], px[(x + 1, y + 1)], px[(x, y + 1)], px[(x - 1, y + 1)], px[(x - 1, y)]]
                if neighborColors.count(on) <= 1:
                    continue
                # D) Is not 8-Simple, removing pixel does affect connectivness of neighboring pixels, therefore don't remove pixel
                if not is8Simple(neighborColors):
                    continue

                # mark pixel i_xy for deletion
                marked_pixels.append((x,y))

                # todo maybe remove
                crop_constraint = (
                    (min(crop_constraint[0][0], x - 1),
                     min(crop_constraint[0][1], y - 1)),
                    (max(crop_constraint[1][0], x + 1),
                     max(crop_constraint[1][1], y + 1))
                )

                pixel_deleted = True
            for i_xy in marked_pixels:
                px[i_xy] = off
        # todo maybe remove
        # bounding_box_of_changes = crop_constraint
        bbox = crop_constraint

    # print("bounding_box_of_changes:",bounding_box_of_changes)
    print("Passes: ", index)
    return im


def is8Simple(neighborColors):
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
    # if not (len(eight_simple) <= 2 or len(eight_simple) == 3 and (eight_simple[0] == off or eight_simple[0] == eight_simple[-1])
    #     or (len(eight_simple) == 4 and neighborColors[0] == off and neighborColors[-1] == neighborColors[1]==on)):


if __name__ == "__main__":
    pr = cProfile.Profile()

    filename = "graphs/lars_graph16.png"
    # threshold = 200
    # # Correct Color-scheme
    # # 1 is part of graph and 0 is background (on monitor, displayed as black background with a with graph)
    # def threshold_function(x): return off if x > threshold else on
    # # def threshold_function(x): return 255 if x > threshold else 0
    # im = Image.open(filename).convert("L").point(threshold_function, mode='1')
    # im = im.crop(im.getbbox())
    # print(im.getbbox())

    # im.show()
    pr.enable()

    im = thining(filename)

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(20)
    # pr.print_stats(sort=2)
    # im.show()
