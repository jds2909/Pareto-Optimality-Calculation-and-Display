# small helpers to keep core algorithms tidy.

import numpy as np

def apply_directions(points, directions):
    # flip any objective marked as 'max' so everything becomes minimisation
    P = np.asarray(points).copy()
    if directions is None:
        return P

    if len(directions) != P.shape[1]:
        raise ValueError("directions length must match number of objectives")

    for j, d in enumerate(directions):
        if str(d).lower().startswith("max"):
            P[:, j] = -P[:, j]
    return P
