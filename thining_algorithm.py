from PIL import Image, ImageOps
import numpy as np


import cProfile
import pstats
on, off = 1, 0
# on, off = 0, 255


def colorPixelLocations(px, color=0, listOfPixels=None, bound=None):
    if listOfPixels is None and bound is not None:
        # When content in bound is unknown
        return [(col, row) for col in range(bound[0][0], bound[1][0]) for row in range(bound[0][1], bound[1][1]) if px[(col, row)] == color]
    elif listOfPixels is not None and bound is None:
        # When black pixels of last pass, across image is known
        return [pixel for pixel in listOfPixels if px[pixel] == color]
    elif listOfPixels is not None and bound is not None:
        # When black pixels of last pass, across image is known and no changes were made outside bound
        return [pixel for pixel in listOfPixels if px[pixel] == color and bound[0][0] <= pixel[0] <= bound[1][0] and bound[0][1] <= pixel[1] <= bound[1][1]]
    else:
        raise AttributeError("listOfPixels and bound can't both be None")


def thining(filename):
    # on is color of graph and off is color of background
    on, off = 1,0
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
    width, height = im.size
    px = im.load()

    # directions = ["N","S","W","E"]
    # coordinate (0,0) is top-left corner
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    # ((1,1),(width-1,height-1))
    image_changeing_bounds = ((1, 1), (width - 1, height - 1))
    blackpixel_coordinates_within_bound = colorPixelLocations(
        px, color=0, bound=image_changeing_bounds)

    pixel_deleted = True
    index = 0
    while pixel_deleted:
        index += 1
        blackpixel_coordinates_within_bound = colorPixelLocations(
            px, color=0, listOfPixels=blackpixel_coordinates_within_bound, bound=image_changeing_bounds)
        # print("Pass: {}, Black pixels: {}, removed: {}".format(index, len(blackpixel_coordinates_within_bound),svarta-len(blackpixel_coordinates_within_bound)))
        # print(image_changeing_bounds)

        crop_constraint = ((width - 1, height - 1), (1, 1))
        pixel_deleted = False
        for i, d in enumerate(directions):
            marked_pixels = []

            # For each pixel i_xy
            for (col, row) in blackpixel_coordinates_within_bound:
                i_xy = (x, y) = (col, row)
                # todo change directions to d[0] and d[1]
                i_d = (col + directions[i][0], row + directions[i][1])

                # A) Pixel is white
                if px[i_xy] == off:
                    continue
                # B) Pixel is black, but not edge in direction
                if px[i_d] == on:
                    continue
                # C) Pixel is an endpoint
                # List of colors of neighbor pixels, start in top-left pixel, end in left pixel
                neighborColors = [px[(x - 1, y - 1)], px[(x, y - 1)], px[(x + 1, y - 1)], px[(
                    x + 1, y)], px[(x + 1, y + 1)], px[(x, y + 1)], px[(x - 1, y + 1)], px[(x - 1, y)]]
                if neighborColors.count(on) <= 1:
                    continue
                # D) Is not 8-Simple, removing pixel does affect connectivness of neighboring pixels, therefore don't remove pixel
                if not is8Simple(neighborColors):
                    continue

                # mark pixel i_xy for deletion
                marked_pixels.append(i_xy)

                crop_constraint = (
                    (min(crop_constraint[0][0], i_xy[0] - 1),
                     min(crop_constraint[0][1], i_xy[1] - 1)),
                    (max(crop_constraint[1][0], i_xy[0] + 1),
                     max(crop_constraint[1][1], i_xy[1] + 1))
                )

                pixel_deleted = True
            # print("Marked pixels: {}".format(len(marked_pixels)))
            for i_xy in marked_pixels:
                px[i_xy] = off
        image_changeing_bounds = crop_constraint

    # print("image_changeing_bounds:",image_changeing_bounds)
    # print("Passes: ", index)
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
    threshold = 200
    # Correct Color-scheme
    # 1 is part of graph and 0 is background (on monitor, displayed as black background with a with graph)
    def threshold_function(x): return 0 if x > threshold else 1
    # def threshold_function(x): return 255 if x > threshold else 0
    im = Image.open(filename).convert("L").point(threshold_function, mode='1')
    im = im.crop(im.getbbox())
    print(im.getbbox())
    im.show()
    pr.enable()
    # import time
    #
    # t0 = time.time()
    im = thining(filename)
    # t1 = time.time()
    #
    # total = t1 - t0
    # print(total)
    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(10)
    # pr.print_stats(sort=2)
    im.show()
