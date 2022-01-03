class priority_node:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.children = []

    def children():
        return children

    def push_children(nodes):
        self.children += node

class priority_queue:
    def __init__(self, size, reference_node):
        self.size = size
        self.reference_node = reference_node
        self.queue_root = None

    def push(node):
        if not self.queue_root:
            self.queue_root = node
            return

        else:
            self.__push(node, [self.queue_root])

    def __push(node, queue_nodes):
        for queue_node in queue_nodes:
            if self.closer_than(node, queue_node):
                self.swap(node, queue_node)
                self.__push(queue_node,
                return
        self.__push(node, next_nodes)

    # returns true if a is closer than b
    def closer_than(node_a, node_b):
        _a = 0
        _b = 0
        for i in range(len(node_a.coordinates)):
           _a += (node_a.coordinates[i]
                  - self.reference_node.coordinates[i]) ** 2
           _b += (node_b.coordinates[i]
                  - self.reference_node.coordinates[i]) ** 2

        dist_a = _a ** 0.5
        dist_b = _b ** 0.5
        return dist_a < dist_b

    def swap(node_a, node_b):
        node_a.set_parent(node_b.get_parent())
        node_a.push_children(node_b.children())



