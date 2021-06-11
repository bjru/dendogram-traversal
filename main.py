from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle, TextFace
import thining_algorithm as t
import graph_finder as gf
import graph_generation as gg
import timeit
import re

on,off = 1,0

def run(filename, rootDirection="n", drawAndPlotTree = (True,True) ,save=False,printResult=False):
    """
    Main function for running the algorithm
    :param filename: file to use for finding the graph struckture
    :param rootDirection: The root is the black pixel closest pixel to this edge. No other pixel is closest to this edge
    :param drawAndPlotTree: Tuple for displaying the resulting image and plotting the corresponding graph
    :param save: Boolean for if resulting image should be stored, if True store at same location as original image
    :param printResult: If true, print resulting newick code
    :return: image object and the newick code
    """
    im = t.thining(filename)
    im.load()

    im, newick = gf.graph_finder(im, rootDirection=rootDirection, varnings=True)

    if save:
        name = filename.split(".")
        name = name[0] + "_post_graphfinder." + name[1]
        im.save(name, "PNG")
    if printResult:
        print("Graph is interpreted in Newick format as:\n", newick)
    if drawAndPlotTree[0]:
        im.show()
    if drawAndPlotTree[1]:
        gg.treePlot(newick)

    return im, newick
def treeFormatTesting(newick):
    """
    Used to clean up newick code for smoother comparison in tests, no leaf names are visible among other things
    :param newick: Newick code
    :return:
    """
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.rotation = 90
    nstyle = NodeStyle()
    nstyle["size"] = 0
    t = Tree(newick)
    for n in t.traverse():
        n.set_style(nstyle)
        if n.is_leaf():
            name_face = TextFace(n.name, fgcolor="white", fsize=10)
            n.add_face(name_face, column=0, position='branch-right')
    return t,ts

def newickStripNames(newick):
    """
    Strips newick code of coordinates
    :param newick: Newick code of format comparable to: "((45_92,(28_182,11_182)18_90)19_1)19_1;"
    :return: Same code but with leaf and internal node names replaced or removed
    """
    P_internalNodes = "(\)\d+_\d+)"
    P_leaf = "(\d+_\d+)"
    return re.sub(P_leaf, "L", re.sub(P_internalNodes, ")", newick))

def testAlgorithmPerformance(ListNewick,filename="graphs/test.png"):
    """
    Prints information about successrate of algorithm under ideal conditions.
    :param ListNewick: List of trees of Newick format
    :param filename: file path to temporary use to store and check (ETE3 stores graph and algorithm checks same graph)
    :return: None
    """
    # For progress tracking
    totalNrTrees = len(ListNewick)
    tenthOfTrees = round(totalNrTrees / 10)
    timerStart = timeit.default_timer()
    print("There are {} trees to handle.".format(totalNrTrees))


    success = 0
    for i,newick in enumerate(ListNewick):

        t,ts = treeFormatTesting(newick)
        # render graph as an image so run() can check the same image
        t.render(file_name=filename, tree_style=ts)
        # Result from algorithm
        _, newickAlg = run(filename=filename, rootDirection="n", drawAndPlotTree=(False, False), save=False)
        # Strips the newick from the algorithm of coordinates before comparison
        newickAlgClean = newickStripNames(newickAlg)


        if newick != newickAlgClean:
            print("Error at index {}".format(i))
            print("Original Newick:       ",newick)
            print("Newick from algorithm: ",newickAlgClean)
            print("Newick from algorithm with coordinates: ",newickAlg)
        else:
            success += 1

        # Progress tracker
        if i % tenthOfTrees == 0:
            print("{}% done".format(10 * (i - (i % tenthOfTrees)) / tenthOfTrees),end=", \t")
            print("Time taken: {0:.2f} seconds".format(timeit.default_timer() - timerStart))
    print("Succesfull attempts: {} of total: {} attempts\nChance of algorithm succeding: {}%".format(success, totalNrTrees, round(100*success/totalNrTrees,2)))

if __name__ == "__main__":
    # filename = "graphs/cross_post_thining.png"
    # filename = "graphs/lars_graph16.png"
    # filename = "graphs/crossY3.png"
    # filename = "graphs/cross2.png"
    # filename = "graphs/pre_thining2.png"
    # filename = "graphs/pre_thining1.png"
    # filename = "graphs/pre_thining7-4neighbors.png"
    # filename = "graphs/pre_thining8-5neighbors.png"
    # filename = "graphs/pre_thining9.png"
    filename = "graphs/test.png"

    # im, newick = run(filename=filename, rootDirection="n", drawAndPlotTree=(False,True),save=False)
    # im, newick = run(filename=filename, rootDirection="n", drawAndPlotTree=(True,True),save=False)
    # gg.plotTree("((45_92,(28_182,11_182)18_90)19_1)19_1;")

    testAlgorithmPerformance(gg.generateAllTrees(10))
    # testAlgorithmPerformance(gg.generateXRandomTrees(50,10))