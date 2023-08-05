from itertools import islice
import numpy as np
from path import path


def load_grids(file_pattern, directory="."):
    files = path(directory).files(file_pattern)

    arrays = [None] * len(files)
    for i, f in enumerate(sorted(files)):
        grid_size = None
        grid_origin = None
        delta = None

        with open(f) as ifp:
            for l in ifp:
                l = l.strip()

                if l.startswith("#"):
                    continue
                elif l.startswith("object 1"):
                    grid_size = np.array([int(x) for x in l.split(" ")[-3:]])
                elif l.endswith("data follows"):
                    break

            if grid_size is None:
                raise "No grid size in file {}".format(f)

            arr = np.loadtxt(islice(ifp, 0, grid_size.prod()))

            if arr.size != grid_size.prod():
                raise "Incorrect number of elements"

            arrays[i] = arr.reshape(grid_size)

    arrays = np.array(arrays)
    arrays = arrays.transpose((1, 2, 3, 0))
    return arrays


# Grid energy functions

def set_point_grid(grid, coords, surface, radius):
    pass
