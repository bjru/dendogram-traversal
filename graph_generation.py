from ete3 import Tree, faces, AttrFace, TreeStyle

def treePlotter(newick):
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
    # Do not add leaf names automatically
    ts.show_leaf_name = False
    # Use my custom layout
    ts.layout_fn = my_layout
    t = Tree(newick, format=8)
    # Tell ETE to use your custom Tree Style
    t.show(tree_style=ts)

from itertools import product
# temp buffer to prevent infinite loop in for worOn..., defined here for risk of undefined after first loop
newList = set()
# L will have all trees in the end
L = {"L","(L,L)"}
# Buffer for trees added in the last insert iteration
lastAddedToL = {"(L,L)"}
# iteration index for times smaller trees are inserted into trees in lastAddedToL
for insert in range(6):
    newList = set()
    # clears buffer lastAddedToL by iterating on all elements in it
    for workOn in lastAddedToL:
        # workOn split into non-leaf components
        holes = workOn.split("L")
        # list of different substitutions to fill the "holes" in holes with
        substitutions = list(product(L, repeat=len(holes)-1))
        for e in substitutions:
            e = list(e)
            # To make lists same length
            e.append("")
            # replaces holes
            k = "".join([str(x) + str(y) for x, y in zip(holes, e)])
            newList.add(k)

    print(insert)
    L.union(lastAddedToL)
    lastAddedToL = newList
    # newList = []
L = L.union(lastAddedToL)
L = L.difference({"L", "(L,L)"})

L2 = set()
for e in L:
    # L.discard(e)
    L2.add(e+";")

print(L2)

#




# if __name__ == "__main__":
#     leaves = 3
#     print(balancedTree(leaves))