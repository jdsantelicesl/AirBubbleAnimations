import numpy as np

with open('zz.DAT', 'r') as file:
    tot_lines = 0
    for line in file:
        tot_lines += 1

    depth = tot_lines / 197128
    if depth != round(depth):
        raise ValueError("file does not contain an even amount of visual slices")
    
    # depth, row, cols || time, y-coord, x-coord
    arr = np.empty((depth, 601, 328))

    i = 0
    j = 0
    k = 0
    for line in file:
        vals = line.strip().split()
        arr[k, j, i] = float(vals[4])

        i += 1
        if i > 
