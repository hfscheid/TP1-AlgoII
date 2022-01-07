#!/usr/bin/env python3

import sys
import json

from xNN import xNN

def get_tags(s):
#    return [float(x) for x in s.split(',')]
    return [x for x in s.split(',')]

def to_tuple(line):
    arr = [float(x) for x in line.split(',')]
    return tuple(arr)

def get_data(datafile):
    data_lines = datafile.readlines()
    data = []
    tags = []
    for line in data_lines:
        if line[0] == '@':
            if '{' in line:
                begin = line.find('{')+1
                end = line.find('}')
                tags = get_tags(line[begin:end])
        else:
            data.append(to_tuple(line))
    return data, tags

def main(num_neighbours, datafile):
    with open(datafile, 'r') as ifile:
        data, tags = get_data(ifile)
    # split data into training set (70%)
    # and testing set (30%)
    delimiter = len(data)*7//10
    xnn = xNN(tags,
              data[:delimiter],
              data[delimiter:])
    outfile_names = []
    outfile_name = datafile.split('.')[0]
    results = []
    for i in range(len(num_neighbours)):
        outfile_names.append(f'{outfile_name}_out_{i}.txt')
        with open(outfile_names[i], 'w') as outfile:
            results.append(xnn.classify(int(num_neighbours[i]), outfile))
            outfile.close()

    with open(f'{outfile_name}_stats.json', 'w') as statsfile:
        json.dump(results, statsfile)
#        for result in results:
#            json.dump(result, statsfile)
#            statsfile.write(str(result))
#            statsfile.write('\n')


main(sys.argv[1:-1], sys.argv[-1])
