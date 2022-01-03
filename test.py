#!/usr/bin/env python3
import kdtree
points = [(1, 2, 3, 1), (2, 1, 3, 1), (3, 1, 2, 1), (1, 3, 2, 1), (3, 2, 1, 1)]
tree = kdtree.KDtree(3, points)
tree.print()
n = tree.lookup((2, 1, 3))
p = n.get_parent()
pp = p.get_parent()
