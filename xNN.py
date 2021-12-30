import kdtree

class xNN:
    def __init__(self, x, train_set, test_set):
        dimensions = len(train_set[0] -1)
        self.tree = kdtree.KDtree(dimensions, train_set)
        self.test_set = test_set

    def nearest_neighbours(self, point):
        neighbours = []

        # first find the starting point in the tree:
        root = self.tree.lookup(point)
        # compare it with it's sibling to get the closest point:

        # rewind to parent, check other child.
        # rewind to parent, check other children.
        # always update the neighbouring radius,
        # compare with nodes to discard branches.
