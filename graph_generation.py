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
#     test

