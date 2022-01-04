#!/usr/bin/env python3

import sys
from xNN import xNN

def get_tags(s):
    return [float(x) for x in s[1:-2].split(',')]

def to_tuple(line):
    arr = [float(x) for x in line.split(',')]
    return tuple(arr)

def get_data(datafile):
    data_lines = datafile.readlines()
    data = []
    tags = []
    for line in data_lines:
        if line[0] == '@':
            words = line.split(' ')
            try:
                if words[1] == 'Class':
                    tags = get_tags(words[2])
            except:
                pass
        else:
            data.append(to_tuple(line))
    return data, tags

def main(num_neighbours, datafile):
    with open(datafile, 'r') as ifile:
        data, tags = get_data(ifile)
#    print(f'tags: {tags}')

    # split data into training set (70%)
    # and testing set (30%)
    delimiter = len(data)*7//10
    xnn = xNN(num_neighbours,
              tags,
              data[:delimiter],
              data[delimiter:])

    with open('output.txt', 'w') as outfile:
        xnn.classify(outfile)
        outfile.close()


main(sys.argv[1], sys.argv[2])
