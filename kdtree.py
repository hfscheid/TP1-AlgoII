class Node:
    def __init__(self, comparator):
        self.comparator = comparator
        self.left = None
        self.right = None

    def type(self):
        return 'Node'

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def set_parent(self, node):
        self.parent = node

    def get_parent(self):
        return self.parent

class Leaf:
    def __init__(self, data_tuple):
        self.coordinates = data_tuple[:-1]
        self.tag = data_tuple[-1]

    def type(self):
        return 'Leaf'



class KDtree:
    def __init__(self, dimensions, points):
#        self.ordered_points = {}
#        for i in range(dimension):
#            self.ordered_points[i] = sorted(points, key=lambda x: x[i])
        self.dimensions = dimensions
        self.points = points
        self.root = self.buildtree(points, 0)

    def buildtree(self, point_range, dimension):
        if len(point_range) == 0:
            return

        if len(point_range) == 2:
            node = Node(point_range[0][dimension])
            left = Leaf(point_range[0])
            right = Leaf(point_range[1])
            node.set_left(left)
            node.set_right(right)
            return node

        elif len(point_range) == 1:
            return Leaf(point_range[0])
        else:
            point_range = sorted(point_range, key=lambda point: point[dimension])
            print(f'point range: {point_range}')
            median_index = self.median_index(point_range)
            print(f'median index: {median_index}')
            next_dimension = (dimension+1) % self.dimensions

            node = Node(point_range[median_index][dimension])
            node.set_left(self.buildtree(point_range[:median_index+1],
                                         next_dimension))
            node.set_right(self.buildtree(point_range[median_index+1:],
                                          next_dimension)) 
            return node

    def median_index(self, point_range):
        return len(point_range)//2

    def print(self):
        self.print_level(0, [self.root])

    def print_level(self, level, nodes):
        if len(nodes) == 0:
            return

        print(f'{level}:',end='\t')
        next_nodes = []
        for node in nodes:
            if node.type() is 'Node':
                print(f'[{node.comparator}]', end=' ')
                next_nodes.append(node.get_left())
                next_nodes.append(node.get_right())
            elif node.type() is 'Leaf':
                print(f'{node.coordinates}', end=' ')
        print('\n')
        self.print_level(level+1, next_nodes)

    def lookup(self, point):
        return self.__lookup(point, self.root, 0)

    def __lookup(self, point, root, dimension):
        if root.type() == 'Leaf':
            return root
        elif point[dimension] <= root.comparator:
            return self.__lookup(point, root.get_left(), (dimension+1)%self.dimensions)
        else:
            return self.__lookup(point, root.get_right(), (dimension+1)%self.dimensions)

    def leaves(self, node):
        # return all leaves branching from this node
        pass
