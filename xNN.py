import heapq
import kdtree

class xNN:
    def __init__(self, tags, train_set, test_set):
        dimensions = len(train_set[0])-1
#        self.x = int(x)
        self.tags = tags
        self.tree = kdtree.KDtree(dimensions, train_set)
        self.test_set = test_set
        self.total_hits = 0
        self.hits = dict.fromkeys(tags)
        for k in self.hits:
            self.hits[k] = 0
        self.occurences = dict.fromkeys(tags)
        for k in self.occurences:
            self.occurences[k] = 0
        self.guesses = dict.fromkeys(tags)
        for k in self.guesses:
            self.guesses[k] = 0

    def nearest_neighbours(self, x, point):
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
            neighbours = heapq.nsmallest(x, neighbours)
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

    def __stats(self, point, result):
        true_tag = str(point[-1])
        self.occurences[true_tag] += 1
        self.guesses[result] += 1
        if true_tag == result:
            self.hits[true_tag] += 1
            self.total_hits += 1

    def classify(self,x, outfile):
        for point in self.test_set:
            result = self.nearest_neighbours(x, point)
            self.__stats(point, result)
            outfile.write(str(point)+'\t\t'+str(result)+'\n')

        result = dict()
        
        # acuracia
        result['accuracy'] = self.total_hits/len(self.test_set)*100
#        outfile.write('Accuracy:\n')
#        outfile.write(f'{self.total_hits} hits.\n'\
#                      f'{self.total_hits/len(self.test_set)*100}% accuracy.\n')
#        outfile.write('\n\n')

        # precisao (considerando classe relevante = 1)
        precision = dict()
        stats = dict()
        for tag in self.tags:
            precision[tag] = self.hits[tag]/self.guesses[tag]*100
            stats['hits'] = self.hits[tag]
            stats['guesses'] = self.guesses[tag]
            precision['stats'] = stats
        result['precision'] = precision
#       outfile.write('Precision:\n')
#        for tag in self.tags:
#            outfile.write(f'Tag: {tag}\n'\
#                          f'hits:\t\t\t{self.hits[tag]}\n'\
#                          f'total guesses:\t\t{self.guesses[tag]}\n'
#                          f'precision:\t\t{self.hits[tag]/self.guesses[tag]*100}%\n')
#            outfile.write('\n')
#        outfile.write('\n')

        # revocacao
        recall = dict()
        stats = dict()
        for tag in self.tags:
            recall[tag] = self.hits[tag]/self.occurences[tag]*100
            stats['hits'] = self.hits[tag]
            stats['occurences'] = self.occurences[tag]
            recall['stats'] = stats
        result['recall'] = recall

#        outfile.write('Recall:\n')
#        for tag in self.tags:
#            outfile.write(f'Tag: {tag}\n'\
#                          f'hits:\t\t\t{self.hits[tag]}\n'\
#                          f'total occurences:\t{self.occurences[tag]}\n'
#                          f'recall:\t\t\t{self.hits[tag]/self.occurences[tag]*100}%\n')
#
#            outfile.write('\n')
#        outfile.write('\n')
        return result
