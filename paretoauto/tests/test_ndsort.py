import numpy as np
from paretoauto.algorithms.ndsort import non_dominated_sort

def test_ranks_exist():
    pts = np.array([[1,5,5],[2,4,5],[5,1,5],[3,3,3]])
    ranks, fronts = non_dominated_sort(pts)
    assert len(ranks) == len(pts)
    assert 0 in ranks
