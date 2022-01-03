import sys
from xNN import xNN

def get_tags(string):
    string = string[1:-1]
    return string.split(',')

def to_tuple(line):
    arr = [float(x) for x in line.split(',')[:-1]]
    arr.append(line.split(',')[-1])
    return tuple(arr)

def get_data(datafile):
    data_lines = datafile.readlines()
    data = []
    tags = []
    for line in data_lines:
        if line[0] == '@':
            words = line.split(' ')
            if words[1] == 'Class':
                tags = get_tags(words[2])
            data_lines.remove(line)
        else:
            data.append(to_tuple(line))
    return data, tags

def main(num_neighbours, datafile):
    data = get_data(datafile)

    # split data into training set (70%)
    # and testing set (30%)
    delimiter = len(data)*7/10
    xnn = xNN(num_neighbours,
              data[:delimiter],
              data[delimiter:])


main(sys.argv[0], sys.argv[1])
