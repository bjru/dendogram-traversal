import thining_algorithm as t
import cProfile,pstats
import math
from PIL import Image,ImageOps

def findRoot(px,searchspace,rootDirection="W"):
    def north(pixels): return min(pixels, key=lambda p: p[1])
    def south(pixels): return max(pixels, key=lambda p: p[1])
    def west(pixels): return min(pixels, key=lambda p: p[0])
    def east(pixels): return max(pixels, key=lambda p: p[0])
    def first(pixels): return pixels[0]

    on,off = 0,255
    potential_roots = [pixel for pixel in searchspace if len(getNeighbors(px,pixel,on)) == 1]
    rootDirection = rootDirection.lower()

    switcher = {"n": north, "s": south, "w": west, "e": east, "first": first}
    func = switcher.get(rootDirection, lambda: "Invalid argument")

    return func(potential_roots)

def getNeighbors(px,coord,color):
    (x, y) = coord
    neighbors = [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    return [pixel for pixel in neighbors if px[pixel] == color]

def getNonArcPixels(px,root,parent=None):
    on,off = 0,255

    # nonArcPixels = [] #todo fixa detta
    nonArcPixels = [root] # root, when starting, will look like an arcpixel as it'll only have 1 neighbor so needs to be added here
    # if parent == None: # todo lägg till detta
    #     parent = root
    #todo för nonArcPixels bygg en (Parent,child) lista typ [((1,1),(50,5)), ...]
    while True:
        # todo kom ihåg att root var svart men blir nu vit
        px[root] = off
        neighbors = getNeighbors(px=px,coord=root,color=on)
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
    on, off = 0, 255
    width, height = im.size
    px = im.load()
    boundary = ((0,0),((width,height)))
    blackPixels = t.colorPixelLocations(px,on,bound=boundary)

    #Gets the root and the nodes
    root = findRoot(px,blackPixels,rootDirection=rootDirection)

    intersectionsAndLeafs = getNonArcPixels(px,root)
    print(intersectionsAndLeafs)
    
    #Prints Black dot at each node (5 pixel square)
    for pixel in intersectionsAndLeafs:
        bound = pixel[0]-2, pixel[1]-2, pixel[0]+2, pixel[1]+2
        im.paste(0,box=(bound))
        # box.close()
    #todo Create json object
    #todo add alternative to control what is collected (Like above)



if __name__ == "__main__":

    im = t.thining("graphs/lars_graph16.png")
    # im = t.thining("pre_thining3.png")
    im.load()
    im.show()
    pr = cProfile.Profile()
    pr.enable()

    graph_finder(im,rootDirection = "n", isDendrogram=True)

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(10)
    # Image.point(im, lambda x: 0)

    im.show()
