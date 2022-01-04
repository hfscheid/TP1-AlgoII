import heapq
import kdtree

class xNN:
    def __init__(self, x, tags, train_set, test_set):
        dimensions = len(train_set[0])-1
        self.x = int(x)
        self.tags = tags
        self.tree = kdtree.KDtree(dimensions, train_set)
        self.test_set = test_set

    def nearest_neighbours(self, point):
        self.reference = point
        neighbours = []

        # first find the starting point in the tree:
        root = self.tree.lookup(point)
        neighbours = [root]
        radius = 0

        # extra variable to stabilize heapq sorting
        counter = 0
        while True:
            # rewind to parent, check other children.
            parent = root.get_parent()
            if not parent:
                break

            neighbours = self.tree.leaves(parent)
            neighbours, counter = self.distances(neighbours, counter)
#            print(f'neighbours: {neighbours}')
            neighbours = heapq.nsmallest(self.x, neighbours)
            heapq.heapify(neighbours)

            # update the neighbouring radius,
            radius = heapq.nlargest(1, neighbours)[0][0]

            # set parent as root for next rewind and
            # compare it with the radius
            root = parent
            dist_to_root = abs(root.value
                    - point[root.dimension])
            if dist_to_root >= radius:
                break

        return self.majority_tag(neighbours)

    def distances(self, neighbours, counter):
        # remove duplicates
#        neighbours = list(dict.fromkeys(neighbours))

        dist_neighbours = []
        for neighbour in neighbours:
            dist_neighbours.append((self.dist(neighbour), counter, neighbour))
            counter += 1

        return dist_neighbours, counter

    def dist(self, neighbour):
        _a = 0
        for i in range(len(neighbour.coordinates)):
            _a += (neighbour.coordinates[i]
                    - self.reference[i]) ** 2
        return _a ** 0.5

    def majority_tag(self, neighbours):
        neighbour_tags = dict.fromkeys(self.tags)
        for tag in self.tags:
            neighbour_tags[tag] = 0
        for n in neighbours:
           neighbour_tags[n[2].value] += 1

        # sort neighbour tags by occurence and
        # pick the greatest one
        neighbour_tags = {
                k: v for k, v in sorted(neighbour_tags.items(),
                                        key=lambda x: x[1],
                                        reverse=True)
        }
        return list(neighbour_tags.keys())[0]

    def classify(self, outfile):
        # for all points in test set
            # do nearest_neighbours
            # print list with all these points and their tags (original vs computed)
        for point in self.test_set:
            result = self.nearest_neighbours(point)
            outfile.write(str(point)+'\t\t'+str(result)+'\n')

