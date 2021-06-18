from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle
import random

def treePlotter(newick, internalNodesHasNames=True):
    """
    Plots the noewick code as a graph
    :param newick: newick code representing a graph
    :param internalNodesHasNames: True if newick format used has names for internal nodes, False otherwise
    :return: None
    """
    ts = TreeStyle()
    ts.rotation = 90

    # If internal nodes have names in the newick format
    if internalNodesHasNames:
        t = Tree(newick, format=8)
        ts.show_leaf_name = False
        def customLayout(n):
            if n.is_leaf():name_face = AttrFace("name") #leafs
            else: name_face = AttrFace("name", fsize=9) #internal node smaller font for text
            # Adds text to graph
            faces.add_face_to_node(name_face, n, column=0, position="branch-right")
        ts.layout_fn = customLayout
    else:
        # Used when internal nodes names are omitted
        t = Tree(newick)
        ts.show_leaf_name = True
        nstyle = NodeStyle()
        nstyle["size"] = 0
        # nstyle["shape"] = "square"
        # nstyle["fgcolor"] = "white"
        for n in t.traverse():
            n.set_style(nstyle)
    t.show(tree_style=ts)

def generateAllTrees(leaves = 5,keepSmallerTrees=False):
    """
    Generates all possible binary graphs, containing x number of leaves, may be slow for larger than 12 leaves
    :param leaves: The number of leaves, the binary tree should use
    :param keepSmallerTrees: True if trees of less leaves should be stored
    :return: List of all trees in newick format
    """
    # L list will have all trees in the end
    L = {"(L,L)"}
    # Buffer for trees added in the last insert iteration
    lastAddedToL = {"(L,L)"}
    # inserts represents how many "(L,L)" are substituted at "L":s  So number of leaves == insert
    for inserts in range(2,leaves):
        tempBuffer = set()
        # clears buffer lastAddedToL by iterating on all elements in it
        for workOn in lastAddedToL:
            #for each "L" in workOn add workOn to Tlist where "L" at holeID is substituted with "(L,L)"
            Tlist = [workOn[:holeID]+"(L,L)"+workOn[holeID+1:] for holeID in [i for i, ltr in enumerate(workOn) if ltr == "L"]]
            tempBuffer.update(Tlist)
        if keepSmallerTrees:
            L.update(lastAddedToL)
        lastAddedToL = tempBuffer
    L.update(lastAddedToL)
    L = L.difference({"L", "(L,L)"})
    return [e+";" for e in L]

def generateXRandomTrees(leaves = 20,trees=10,seed=None):
    """
    Generates a random subset of trees of x leaves, much faster than taking all trees
    :param leaves: number of leaves for the trees
    :param trees: number of trees to be stored at each iteration
    :param seed: if != None: seed to use for the random function to generate the same trees each time function is run
    :return: List of trees with x number of leaves
    """
    if seed is not None:
        random.seed(seed)
    # Buffer for trees added in the last insert iteration
    lastAddedTrees = {"(L,L)"}
    # inserts represents how many "(L,L)" are substituted at "L":s  So number of leaves == insert
    for inserts in range(2,leaves):
        tempBuffer = set()
        # clears buffer lastAddedTrees by iterating on all elements in it
        for workOn in lastAddedTrees:
            #for each "L" in workOn add workOn to a list where "L" at holeID is substituted with "(L,L)", then add them to tempBuffer
            tempBuffer.update([workOn[:holeID]+"(L,L)"+workOn[holeID+1:] for holeID in [i for i, ltr in enumerate(workOn) if ltr == "L"]])
        # If too many trees, pick which ones to keep
        if len(tempBuffer) > trees:
            keepThese = random.sample(range(0, len(tempBuffer)-1), trees)
            lastAddedTrees = set([e for i,e in enumerate(tempBuffer) if i in keepThese])
        else:
            lastAddedTrees = tempBuffer
    return [e+";" for e in lastAddedTrees.difference({"(L,L)"})]


if __name__ == "__main__":
    # leaves = 14
    # pr = cProfile.Profile()
    # pr.enable()
    # T = generateXRandomTrees(leaves=50,trees=10)
    # # T = generateAllTrees(leaves, keepSmallerTrees = False)
    # print(T)
    # print("#Elements: ",len(T))
    # print("First element: ", T[0])
    # print("First element #leaves: ", len([i for i, ltr in enumerate(T[0]) if ltr == "L"]))
    #
    # pr.disable()
    # stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    # stats.print_stats(10)

    treePlotter("((45_92,(28_182,11_182)18_90)19_4)19_1;", True)




