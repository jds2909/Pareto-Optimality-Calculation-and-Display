""" selector chooses which pareto algorithm to use based on the dataset shape
rules simple for now:
    if there are exactly 2 objectives use the fast exact 2d sweep for front 0
    if 3 or more objectives use \non dominated sorting to rank all points
"""

import numpy as np
from .algorithms.pareto2d import pareto_front_indices_2d
from .algorithms.ndsort import non_dominated_sort
from .utils import apply_directions

def sort_fronts(points, directions=None):
    """ auto select algorithm and return ranks fronts and info

    parameters
    points array like n by m objective values for n items and m objectives assumes minimisation
    directions list of 'min' or 'max' optional flips any 'max' columns to '-values' so all are minimised

    returns
    ranks n array rank 0 is pareto optimal front 0 1 is next layer and so on
    fronts list of lists indices grouped by front where front 0 is the best
    info dict which algo was used and if it's approximate false here
    """

    # normalise directions so algorithms only see 'min'
    P = apply_directions(points, directions)
    n, m = P.shape

    # for 2 objectives, peel fronts one at a time using the fast 2d sweep
    if m == 2:
        ranks = np.empty(n, dtype=int)
        fronts = []
        remaining = list(range(n))
        r = 0
        while remaining:
            local_f0 = pareto_front_indices_2d(P[remaining])
            global_f0 = [remaining[i] for i in local_f0]
            fronts.append(global_f0)
            for i in global_f0:
                ranks[i] = r
            keep = set(global_f0)
            remaining = [i for i in remaining if i not in keep]
            r += 1
        info = {"algo": "2d_sweep", "approx": False}
        return ranks, fronts, info

    # for 3+ objectives, non dominated sorting to get all fronts
    ranks, fronts = non_dominated_sort(P)
    info = {"algo": "ndsort_loopy", "approx": False}
    return ranks, fronts, info
