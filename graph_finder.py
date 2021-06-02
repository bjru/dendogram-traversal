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

def getNonMaskedNeighbors(px,i_xy,maskArray):
    (x, y) = i_xy
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    # todo remove this comment --------- To see colors of each neighbor use: [(px[i], i) for i in neighbors]
    # b=0
    # todo kan detta effektiviseras?
    # a=0
    # A = [(x,y) for (x,y) in neighbors if px[(x,y)] == on]
    A = [(x,y) for (x,y) in neighbors if px[(x,y)] == on and not ma.is_masked(maskArray[y,x])]

    # B = [(xn,yn) for (xn,yn) in neighbors if px[(xn,yn)] == on]
    # C = [(maskArray[yn, xn], (xn, yn)) for (xn, yn) in neighbors if px[(xn, yn)] == on]
    # D = [(px[xn,yn],(xn,yn)) for (xn,yn) in neighbors]

    return A


def getNonArcPixels(px,nonArcPixels,root,maskArray, varnings=True):

    (x,y) = root
    # if parent == None: # todo lägg till detta
    #     parent = root
    #todo för nonArcPixels bygg en (Parent,child) lista typ [((1,1),(50,5)), ...]
    while True:
        # px[root] = off #Todo ta bort detta men se till så den inte går bakåt
        maskArray[y,x] = ma.masked
        # Todo Tar just nu neighbors i ordning höger till vänster när nedanför
        neighbors = getNonMaskedNeighbors(px,root,maskArray)
        # if neighbor is non-arc pixel. An arc-pixel is a pixel between intersections or endpoints
        nL = len(neighbors)
        if  nL == 1:
            # If pixel is an arc-pixel => neighbors only contain 1 element => first element is the only element
            (x,y) = root = neighbors[0]
        else:
            # nL == 0 or nL == 2
            nonArcPixels.append(root) #todo ta bort
            # End Point
            if nL == 0:
                return nonArcPixels
            # Handles problems with cases too many neighbors
            elif varnings and nL >= 3: print("Varning, at (x,y)=({},{}), 4 edges neighboring a vertex, output will be incorrect.".format(x,y))
            # elif nL in (2,3):
            for neighbor in neighbors:
                (xn,yn) = neighbor
                if varnings and ma.is_masked(maskArray[yn,xn]):
                    print("Varning, at (x,y)=({},{}), Cycle appears in the graph, output will be incorrect.".format(xn,yn))
                nonArcPixels.extend(getNonArcPixels(px,[], neighbor,maskArray))

            return nonArcPixels
        # todo lägga till vid större korsningar:
        #  else: raise Exception("Too many neighbors when the number is {}, something is wrong at pixel {}".format(nL,root))



def graph_finder(im,rootDirection = "w", varnings=True):
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

    # root, when starting, will look like an arcpixel as it only has 1 neighbor therefore, we need to added it in list
    nonArcPixels = [root]
    # px[3,3] = 0
    im.show()
    intersectionsAndLeafs = getNonArcPixels(px,nonArcPixels, root, maskArray, varnings)
    print(intersectionsAndLeafs)
    print()
    print("För Y ska det bli:",[(3,1), (3,2), (5,3), (1,3)])

    #Prints Black dot at each node (5 pixel square)
    # print(np.asarray(im))
    print()
    im = im.convert("RGB")
    # px = im.load()
    # print(np.asarray(im))
    # print()
    # px[(1,1)] = 100
    # print(np.asarray(im))
    # im.paste(100, box=(0,0,1,1))
    # print(np.asarray(im))
    # im.show()
    # print(np.asarray(im))
    sNB=1
    color = "#FF4949" #Red
    for pixel in intersectionsAndLeafs:
        # nodeBox = pixel[0]-2, pixel[1]-2, pixel[0]+2, pixel[1]+2
        # im.paste(on,box=(nodeBox))
        if sNB ==1:
            nodeBox = pixel[0]-sNB, pixel[1]-sNB, pixel[0]+sNB, pixel[1]+sNB
        else:
            nodeBox = pixel[0], pixel[1], pixel[0]+1, pixel[1]+1
        im.paste(color,box=(nodeBox))
        # box.close()
    #todo Create Newick file or json object
    #todo add alternative to control what is collected (Like above)

    # Must be returned because im.convert("L") creates new variable not avalible in main scope
    return im


threshold = 200
def threshold_function(x):
    return off if x < threshold else on

if __name__ == "__main__":

    # filename = "graphs/cross_post_thining.png"
    # filename = "graphs/lars_graph16.png"
    # filename = "graphs/crossY3.png"
    filename = "graphs/cross2.png"
    # filename = "graphs/pre_thining3.png"
    # filename = "graphs/pre_thining1.png"
    performeThining = True


    if performeThining:
        im = t.thining(filename)
    else:
        im = Image.open(filename).convert("L").point(threshold_function, mode='1')

    im.load()
    pr = cProfile.Profile()
    pr.enable()

    im = graph_finder(im,rootDirection = "w", varnings=True)
    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(15)

    # im.show()
    name = filename.split(".")
    name = name[0] + "_post_graphfinder."+name[1]
    # print(np.asarray(im))
    im.save(name, "PNG")
