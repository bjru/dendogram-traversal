from ete3 import Tree, faces, AttrFace, TreeStyle, NodeStyle
import cProfile,pstats
import random


def treePlotterNames(newick):
    # Taken from http://etetoolkit.org/docs/latest/faqs/#how-do-i-visualize-internal-node-names
    # Used to plot names of internal nodes in ETE3
    def my_layout(node):
        if node.is_leaf():
            # If terminal node, draws its name
            name_face = AttrFace("name")
        else:
            # If internal node, draws label with smaller font size
            name_face = AttrFace("name", fsize=10)
        # Adds the name face to the image at the preferred position
        faces.add_face_to_node(name_face, node, column=0, position="branch-right")
    ts = TreeStyle()
    ts.rotation = 90
    # Do not add leaf names automatically
    ts.show_leaf_name = False
    # Use my custom layout
    ts.layout_fn = my_layout
    t = Tree(newick, format=8)
    # Tell ETE to use your custom Tree Style
    t.show(tree_style=ts)

def treePlotterSimple(newick):
    # Used when internal nodes names are omitted
    t = Tree(newick)
    ts = TreeStyle()
    ts.show_leaf_name = True
    ts.rotation = 90
    nstyle = NodeStyle()
    nstyle["size"] = 0
    # nstyle["shape"] = "square"
    # nstyle["fgcolor"] = "white"
    for n in t.traverse():
        n.set_style(nstyle)
    t.show(tree_style=ts)

def treePlot(newick):
    try:
        treePlotterNames(newick)
    except AttributeError:
        treePlotterSimple(newick)

def generateAllTrees(leaves = 5,keepSmallerTrees=False):
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
    leaves = 14
    pr = cProfile.Profile()
    pr.enable()
    T = generateXRandomTrees(leaves=50,trees=10)
    # T = generateAllTrees(leaves, keepSmallerTrees = False)
    print(T)
    print("#Elements: ",len(T))
    print("First element: ", T[0])
    print("First element #leaves: ", len([i for i, ltr in enumerate(T[0]) if ltr == "L"]))

    pr.disable()
    stats = pstats.Stats(pr).strip_dirs().sort_stats('cumtime')
    stats.print_stats(10)




