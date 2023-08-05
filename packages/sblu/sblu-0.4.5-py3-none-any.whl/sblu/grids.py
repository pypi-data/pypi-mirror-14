from itertools import islice
import numpy as np


def load_grid(file_path):
    with open(file_path, 'r') as ifp:
        return load_grid_stream(ifp)


def load_grid_stream(ifp):
    grid_size = None
    grid_origin = None

    for l in ifp:
        l = l.strip()

        if l.startswith("#"):
            continue
        elif l.startswith("object 1"):
            grid_size = np.array([int(x) for x in l.split(" ")[-3:]])
        elif l.startswith("origin"):
            grid_origin = np.array([float(x) for x in l.split(" ")[-3:]])
        elif l.endswith("data follows"):
            break

    if grid_size is None:
        raise "No grid size in file {}".format(f)

    arr = np.loadtxt(islice(ifp, 0, grid_size.prod()))

    if arr.size != grid_size.prod():
        raise "Incorrect number of elements"

    arr = arr.reshape(grid_size)

    return arr, grid_origin
