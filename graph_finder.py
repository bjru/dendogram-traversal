import thining_algorithm as t
import cProfile,pstats
import math
from PIL import Image,ImageOps
import numpy as np
import numpy.ma as ma

# 1 is part of graph and 0 is background (on monitor, displayed as black background with a white graph and text)
on,off = 1,0


def findRoot(px,searchspace,rootDirection="W"):
    rootDirection = rootDirection.lower()
    # p = (x,y)
    # switcher takes the pixel with largest or smallest x or y-coordinate from the list of the non-background pixels,
    # based on a direction choosen (should be the root of the graph to have any meaning)
    switcher = {"n": lambda pixels : min(pixels, key=lambda p: p[1]),
                "s": lambda pixels : max(pixels, key=lambda p: p[1]),
                "w": lambda pixels : min(pixels, key=lambda p: p[0]),
                "e": lambda pixels : max(pixels, key=lambda p: p[0]),
                "first": lambda pixels : pixels[0]}
    func = switcher.get(rootDirection, lambda: "Invalid argument")
    return func(searchspace)

def getNeighbors(px,i_xy):
    (x, y) = i_xy
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    # todo remove this comment --------- To see colors of each neighbor use: [(px[i], i) for i in neighbors]

    # todo kan detta effektiviseras?
    return [pixel for pixel in neighbors if px[pixel] == on]

def getNonArcPixels(px,maskArray,root,parent=None):
    # nonArcPixels = [] #todo fixa detta
    # root, when starting, will look like an arcpixel as it only has 1 neighbor therefore, we need to added it in list

    (x,y) = root
    nonArcPixels = [root]
    # if parent == None: # todo lägg till detta
    #     parent = root
    #todo för nonArcPixels bygg en (Parent,child) lista typ [((1,1),(50,5)), ...]
    while True:
        # todo kom ihåg att root var svart men blir nu vit
        px[root] = off
        maskArray[y,x] = ma.masked
        neighbors = getNeighbors(px,root)
        # if neighbor is non-arc pixel. An arc-pixel is a pixel between intersections or endpoints
        if len(neighbors) != 1:
            nonArcPixels.append(root) #todo ta bort
            # End Point
            if len(neighbors) == 0:
                return nonArcPixels
            # elif len(neighbors) in (2,3):
            for neighbor in neighbors:
                nonArcPixels.extend(getNonArcPixels(px,neighbor))
            return nonArcPixels
            # else: raise Exception("Too many neighbors when the number is {}, something is wrong at pixel {}".format(len(neighbors),root))
        else:
            root = neighbors[0]



def graph_finder(im,rootDirection = "w",isDendrogram=True):
    """
    Main function for graph finding
    :param im:
    :param rootDirection:
    :param isDendrogram:
    :return:
    """
    # Used to access pixel data
    px = im.load()
    # Converts image into a Numpy array, then creates a mask of the Numpy array, used to mask away background pixels and
    # pixels which should not be removed
    maskArray = ma.masked_equal(np.asarray(im), off)

    # All non-background pixels
    nonzero = np.nonzero(maskArray)
    nonzero_indices = [(x,y) for (y, x) in zip(nonzero[0], nonzero[1])]


    #Gets the root and the nodes
    root = findRoot(px,nonzero_indices,rootDirection=rootDirection)

    intersectionsAndLeafs = getNonArcPixels(px,maskArray,root)
    print(intersectionsAndLeafs)
    
    #Prints Black dot at each node (5 pixel square)
    for pixel in intersectionsAndLeafs:
        nodeBox = pixel[0]-2, pixel[1]-2, pixel[0]+2, pixel[1]+2
        im.paste(on,box=(nodeBox))
        # box.close()
    #todo Create Newick file or json object
    #todo add alternative to control what is collected (Like above)



if __name__ == "__main__":

    filename = "graphs/post_thining1.png"
    # im = t.thining("graphs/lars_graph16.png")
    # im = t.thining("pre_thining3.png")
    threshold = 200
    def threshold_function(x):
        return off if x < threshold else on
    im = Image.open(filename).convert("L").point(threshold_function, mode='1')
    im.load()
    # im.show()
    pr = cProfile.Profile()
    pr.enable()

    graph_finder(im,rootDirection = "n", isDendrogram=True)

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(15)
    # Image.point(im, lambda x: 0)

    im.show()
