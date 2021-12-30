def to_tuple(line):
    arr = [float(x) for x in line.splt(',')]
    return tuple(arr)

def get_data(datafile):
    data_lines = datafile.readlines()
    data = []
    for line in data_lines:
        if line[0] == '@':
            data_lines.remove(line)
        else:
            data.append(to_tuple(line))
    return data

def main(datafile)
