# pareto front 0 for 2D minimisation simple & exact
# sort by obj1 (ascending), sweep on Obj2

import numpy as np

def pareto_front_indices_2d(points):
    pts = np.asarray(points)
    order = np.argsort(pts[:, 0], kind="mergesort")
    x_sorted = pts[order]
    best = np.inf
    keep_local = []
    for i, (_, y) in enumerate(x_sorted):
        if y < best:
            best = y
            keep_local.append(i)
    return order[keep_local]
