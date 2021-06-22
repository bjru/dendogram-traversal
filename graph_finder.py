import thining_algorithm as t
import warnings
import cProfile,pstats
import math
from math import floor,ceil
from PIL import Image
import numpy as np
import numpy.ma as ma

import graph_generation

# 1 is part of graph and 0 is background (on monitor, displayed as black background with a white graph and text)
on,off = 1,0


def findRoot(px,searchspace,rootDirection="n"):
    """
    Finds the pixel (in the graph) that is closest to a specific edge
    :param px: pixel object for getting/changing color values of pixels
    :param searchspace: A list of all pixels part of the graph (or has same color as graph)
    :param rootDirection: One of four directions (n, s, w, e, "first" pixel in list) root is choosen as the pixel closest to this direction
    :return: A pixel coordinate representing the choosen root
    """
    rootDirection = rootDirection.lower()
    # switcher takes the pixel with largest or smallest x or y-coordinate from the list of the non-background pixels,
    # based on a direction choosen (should be the root of the graph to have any meaning)
    switcher = {"n": lambda pixels : min(pixels, key=lambda p: p[1]),
                "s": lambda pixels : max(pixels, key=lambda p: p[1]),
                "w": lambda pixels : min(pixels, key=lambda p: p[0]),
                "e": lambda pixels : max(pixels, key=lambda p: p[0]),
                "first": lambda pixels : pixels[0]}
    func = switcher.get(rootDirection, lambda: "Invalid argument")
    return func(searchspace)

def getNonMaskedNeighbors(px,i_xy,maskArray):
    """
    Gets a coordinate list of all neighboring pixels with same color as graph (all should be part of the graph)
    :param px: pixel object for getting/changing color values of pixels
    :param i_xy: coordinates of a center pixel
    :param maskArray: Numpy masked array used to select unmasked pixels to use in algorithm
    :return: A list of all neighbors to i_xy which have the same color as i_xy/the graph and are not masked
    """
    (x, y) = i_xy
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    A = [(x,y) for (x,y) in neighbors if px[(x,y)] == on and not ma.is_masked(maskArray[y,x])]

    return A

def getAdjacencySet(neighbors, maskArray):
    """
    Gets all neighbors to given parameter neighbors
    :param neighbors: A list of pixels neighboring a common vertex
    :param maskArray: Numpy masked array used to select unmasked pixels to use in algorithm
    :return: returns a set of pixels adjacent to the pixels in neighbors, none of pixels in neighbors is returned
    """
    n = neighbors
    nL = len(n)
    adjacent = set()
    for i in range(nL - 1):
        for j in range(i + 1, nL):
            if math.dist(n[i], n[j]) <= 1.42:
                adjacent = adjacent.union([n[i], n[j]])
                maskArray[n[i][1], n[i][0]] = maskArray[n[j][1], n[j][0]] = ma.masked
    return adjacent
def joinAdjacentNeighbors(px,root, neighbors, maskArray,varnings=True):
    """
    Joins neighbors, which makes a length 3 cycle together, into a single vertex by returning a list of non-adjacent neighbors.
    Note that # 1.42 is an approximation and upperbound to math.sqrt(2) used for distance comparisons
    :param px: pixel object for getting/changing color values of pixels
    :param root: pixel coordinate choosen as a vertex
    :param neighbors: A list of pixels neighboring a common vertex (root)
    :param maskArray: Numpy masked array used to select unmasked pixels to use in algorithm
    :param varnings: Boolean of whether to display some warnings
    :return: Set of neighbors to root that are not adjacent (these may be neighbors neighbors etc...)
    """
    # Adds neighbors with adjacency relation together into the set: adjacent
    adjacent = getAdjacencySet(neighbors, maskArray)
    while True:
        neighbors = set(neighbors).difference(adjacent) # All neighbors, of root, not adjacent to any other neighbor added to set first
        for p in adjacent:
            neighbors = neighbors.union(getNonMaskedNeighbors(px, p, maskArray))
        # check no pixel in neighbors are adjacent
        adjacent = getAdjacencySet(list(neighbors), maskArray)
        if len(adjacent) == 0: break

    if varnings and len(neighbors) >= 3:
        warnings.warn("At (x,y)=({},{}), 4 edges neighboring a vertex, output will be incorrect.".format(root[0],root[1]))

    return neighbors

# def getNonArcPixels(px,nonArcPixels,root,maskArray, newick, varnings=True):
# def getNonArcPixels(px,nonArcPixels,root,maskArray,rootDirection, varnings=True):
def getNonArcPixels(px,nonArcPixels,root,maskArray,rootDirection, varnings, possibleThresholds,grayPx):
    # newick = ""
    (x,y) = root
    # todo change
    lastAdded = -1
    while True:
        # todo change
        gray = grayPx[x-1,y-1]
        if lastAdded != gray:
            # if gray == 255: print("White at:", root)
            possibleThresholds.add(gray)
            lastAdded = gray


        maskArray[y,x] = ma.masked
        neighbors = getNonMaskedNeighbors(px,root,maskArray)
        nL = len(neighbors)

        # Arcpixel, START===========
        if  nL == 1: # Arc Pixel, should be ignored
            (x,y) = root = neighbors[0]
            continue

        nonArcPixels.append(root)
        if nL == 0:  # End Point
            newick = "{}_{},".format(x,y)
            # todo change
            # return nonArcPixels, newick
            return nonArcPixels, newick, possibleThresholds
        elif nL >= 2:  # May be an intersection,
            # nL should be 2<=x<=5
            neighbors = joinAdjacentNeighbors(px,root, neighbors, maskArray)

        # newick += "("
        newick = ""
        # Order of neighbors based on root direction:
        # For Newick code to adher to same order as viewed in image
        # Sorting direction of neighbors follows logic below:
        # rootDirection: n -> min(x), s -> max(x), w -> min(y), e -> max(y)
        switcher = {"n": (lambda p: p[0],True), "s": (lambda p: p[0],False), "w": (lambda p: p[1],False), "e": (lambda p: p[1],True)}
        sortDir = switcher.get(rootDirection, lambda: "Invalid argument")
        neighbors = sorted(neighbors, key=sortDir[0],reverse=sortDir[1])

        for neighbor in neighbors:
            (xn, yn) = neighbor
            if varnings and ma.is_masked(maskArray[yn, xn]):
                warnings.warn("At (x,y)=({},{}), 4 edges neighboring a vertex, output will be incorrect.".format(xn,yn))
            # todo change
            # childNonArc, newickChild = getNonArcPixels(px, [], neighbor, maskArray,rootDirection)
            childNonArc, newickChild, extraThresh = getNonArcPixels(px, [], neighbor, maskArray,rootDirection,varnings, possibleThresholds,grayPx)
            possibleThresholds.update(extraThresh)
            # todo changes END
            nonArcPixels.extend(childNonArc)
            newick += newickChild

        # If part of a cycle and all neighbors of pixel are already masked and used in construction of newick code
        # (incorrect for the purpose of being a tree but returns error if not dealt with)
        if len(newick) == 0:
            warnings.warn("Pixel at (x,y)={}, is not a leaf, it's part of a cycle and all neighbors are already handled.".format(root))
            newick = "{}_{},".format(x, y)
        if newick[-1] != ",":
        # if newick[-1] != ",":
            warnings.warn("warning missing ',' for (x,y)="+root)
        newick = "(" + newick[0:-1] + "){}_{},".format(root[0], root[1])
        # return nonArcPixels, newick
        # todo change
        # return nonArcPixels, newick
        return nonArcPixels, newick, possibleThresholds

# def graph_finder(im,rootDirection = "n", varnings=True, nodeDiameter=1,color = "#FF4949"):
def graph_finder(im,grayImage,rootDirection = "n", varnings=True, nodeDiameter=1,color = "#FF4949"):
    """
    Main function for graph finding
    :param im: image object containng the graph
    :param rootDirection: One of four directions (n, s, w, e, "first" pixel in list) root is choosen as the pixel closest to this direction
    :param varnings: Boolean of whether to display some warnings
    :return: returns the image object an a string in Newick format
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


    # root, when starting, will look like an arcpixel as it only has 1 neighbor therefore, we need to added it in list
    nonArcPixels = [root]

    # todo some changes
    # intersectionsAndLeafs, newick = getNonArcPixels(px,nonArcPixels, root, maskArray, rootDirection, varnings)
    grayPx = grayImage.load()
    possibleThresholds = set([grayPx[root[0]-1,root[1]-1]])
    intersectionsAndLeafs, newick, possibleThresholds = getNonArcPixels(px,nonArcPixels, root, maskArray, rootDirection, varnings, possibleThresholds,grayPx)
    # todo some changes END

    newick = newick[0:-1] if newick[-1] == "," else newick

    # Solution for if root and first intersection are the same, may happen when root in image occurs on an arc-pixel
    # instead of a terminal node
    rootPos="{}_{}".format(root[0],root[1])
    if newick[-len(rootPos):] != rootPos:
        newick = "(" + newick + "){};".format(rootPos)
    else:
        newick += ";"


    im = im.convert("RGB")
    d = abs(nodeDiameter)

    for pixel in intersectionsAndLeafs:
        nodeBox = pixel[0]-floor(d/2), pixel[1]-floor(d/2), pixel[0]+ceil(d/2), pixel[1]+ceil(d/2)
        im.paste(color,box=(nodeBox))
    # todo change
    # return im, newick
    return im, newick, possibleThresholds



if __name__ == "__main__":

    # filename = "graphs/cross_post_thining.png"
    # filename = "graphs/lars_graph16.png"
    # filename = "graphs/crossY3.png"
    # filename = "graphs/cross2.png"
    # filename = "graphs/pre_thining2.png"
    # filename = "graphs/pre_thining1.png"
    # filename = "graphs/test2.png"
    # filename = "graphs/pre_thining7-4neighbors.png"
    # filename = "graphs/pre_thining8-5neighbors.png"
    filename = "graphs/lars_graph12_FIX.png"
    performeThining = True
    drawTree = False
    threshold = 130


    imGray = Image.open(filename).convert("L")
    if performeThining:
        im = t.thining(filename,threshold=threshold, viewBeforeThining=True)
    else:
        im = imGray.point(lambda x : off if x < threshold else on, mode='1')
    im.load()

    pr = cProfile.Profile()
    pr.enable()

    # im, newick = graph_finder(im, rootDirection="w", varnings=True, nodeDiameter=1, color="#FF4949")
    im, newick,possibleThresholds = graph_finder(im,grayImage=imGray, rootDirection="w", varnings=True, nodeDiameter=1, color="#FF4949")

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(15)

    name = filename.split(".")
    name = name[0] + "_post_graphfinder."+name[1]
    # print(np.asarray(im))
    im.save(name, "PNG")
    print("Graph is interpreted in Newick format as:\n",newick)
    if drawTree:
        im.show(title="Testing graph_finder")
        graph_generation.treePlotter(newick, internalNodesHasNames=False)

    # todo change
    # print("If problems occured with part of graph missing, try a higher threshold.\nIf you need a better threshold, try one of:")
    print("If problems occured with part of graph missing, try a higher threshold.\nIf you need a better threshold, try one of:",possibleThresholds)


