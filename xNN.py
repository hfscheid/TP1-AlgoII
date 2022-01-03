import heapq
import kdtree

class xNN:
    def __init__(self, x, train_set, test_set):
        dimensions = len(train_set[0])-1
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
            if not parent:
                break

            neighbours = self.tree.leaves(parent)
            neighbours = self.distances(neighbours)
            neighbours = heapq.nsmallest(self.x, neighbours)
            heapq.heapify(neighbours)

            # update the neighbouring radius,
            print(f'neighbours: {neighbours}')
            radius = heapq.nlargest(1, neighbours)[0][0]

            # set parent as root for next rewind and
            # compare it with the radius
            root = parent
            dist_to_root = abs(root.value
                    - point[root.dimension])
            if dist_to_root >= radius:
                break

        return self.majority_tag(neighbours)

    def distances(self, neighbours):
        # remove duplicates
#        neighbours = list(dict.fromkeys(neighbours))

        dist_neighbours = []
        for neighbour in neighbours:
            dist_neighbours.append((self.dist(neighbour), neighbour))

        return dist_neighbours

    def dist(self, neighbour):
        _a = 0
        for i in range(len(neighbour.coordinates)):
            _a += (neighbour.coordinates[i]
                    - self.reference[i]) ** 2
        return _a ** 0.5

    def majority_tag(neighbours):
        neighbour_tags = dict()
        for tag in self.tags:
            neighbour_tags[tag] = 0
        for n in neighbours:
           neighbour_tags[neighbour.value] += 1


