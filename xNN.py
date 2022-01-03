import heapq
import kdtree

class xNN:
    def __init__(self, x, train_set, test_set):
        dimensions = len(train_set[0] -1)
        self.x = x
        self.tree = kdtree.KDtree(dimensions, train_set)
        self.test_set = test_set

    def nearest_neighbours(self, point):
        self.reference = point
        neighbours = []

        # first find the starting point in the tree:
        root = self.tree.lookup(point)
        neighbours = [root]
        radius = 0
        while True:
            # rewind to parent, check other children.
            parent = root.get_parent()
            neighbours.add(parent.leaves())
            neighbours = self.distances(neighbours)
            neighbours = heapq.nsmallest(self.x, neighbours)
            neighbours = heapq.heapify(neighbours)

            # update the neighbouring radius,
            radius = heapq.nlargest(1, neighbours)[0]

            # set parent as root for next rewind and
            # compare it with the radius
            root = parent
            dist_to_root = abs(root.comparator
                    - point.coordinates[root.dimension])
            if dist_to_root >= radius:
                break

    def distances(neighbours):
        # remove duplicates
        neighbours = list(set(neighbours))

        dist_neighbours = []
        for neighbour in neighbours:
            dist_neighbours.append(self.dist(neighbour), neighbour)

        return dist_neighbours

    def dist(neighbour):
        _a = 0
        for i in range(len(neighbour.coordinates)):
            _a += (neighbour.coordinates[i]
                    - self.reference.coordinates[i]) ** 2
        return _a ** 0.5
