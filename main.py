from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle, TextFace
import thining_algorithm as t
import graph_finder as gf
import graph_generation as gg
import timeit
import re

on,off = 1,0

def run(filename, rootDirection="n", drawAndPlotTree = (True,True) ,saveName=None,printResult=False):
    im = t.thining(filename)
    im.load()

    im, newick = gf.graph_finder(im, rootDirection=rootDirection, varnings=True)

    if saveName is not None :
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
def treeFormat(newick):
    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.rotation = 90
    nstyle = NodeStyle()
    nstyle["size"] = 0
    rstyle = NodeStyle()
    rstyle["size"] = 0
    rstyle["shape"] = "circle"
    rstyle["fgcolor"] = "black"

    t = Tree(newick)
    for n in t.traverse():
        n.set_style(nstyle)
        if n.is_leaf():
            name_face = TextFace(n.name, fgcolor="white", fsize=10)
            n.add_face(name_face, column=0, position='branch-right')
        elif n.is_root():
            n.set_style(rstyle)
    return t,ts

def newickStripNames(newick):
    P_internalNodes = "(\)\d+_\d+)"
    P_leaf = "(\d+_\d+)"
    return re.sub(P_leaf, "L", re.sub(P_internalNodes, ")", newick))

def testAlgorithmPerformance(ListNewick,filename="graphs/test.png"):
    # For progress tracking
    totalNrTrees = len(ListNewick)
    tenthOfTrees = round(totalNrTrees / 10)
    timerStart = timeit.default_timer()
    print("There are {} trees to handle.".format(totalNrTrees))


    success = 0
    for i,newick in enumerate(ListNewick):

        t,ts = treeFormat(newick)
        # render graph as an image so run() can check the same image
        t.render(file_name=filename, tree_style=ts)
        _, newickAlg = run(filename=filename, rootDirection="n", drawAndPlotTree=(False, False), saveName=None)
        # Strips the newick from the algorithm of coordinates before comparison
        newickAlgClean = newickStripNames(newickAlg)

        # Availble to look at the graphs of both original newick and graph:s newick
        # t.show(tree_style=ts)
        # t2,ts2 = treeFormat(newickAlgClean)
        # t2.show(tree_style=ts2)

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

        # print("=========Start============")
        # print("Newick:               ",newick)
        # # if newickAlgClean[0] == "(" and newickAlgClean[-2] == ")":
        #     # newickAlg = newickAlg[1:-2]+";"
        # print("Newick from algorithm:",newickAlgClean)
        # print("Newick from algorithm with internal:",newickAlg)
        # print("=========End==============")

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

    # im, newick = run(filename=filename, rootDirection="n", drawAndPlotTree=(False,True),saveName=None)
    # im, newick = run(filename=filename, rootDirection="n", drawAndPlotTree=(True,True),saveName=None)
    # gg.plotTree("((45_92,(28_182,11_182)18_90)19_1)19_1;")

    # testAlgorithmPerformance(gg.generateAllTrees(7))
    testAlgorithmPerformance(gg.generateXRandomTrees(50,10))