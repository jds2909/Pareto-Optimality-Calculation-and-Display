import numpy as np
from paretoauto.algorithms.pareto2d import pareto_front_indices_2d

def test_simple_2d():
    pts = np.array([[1,5],[2,4],[3,3],[4,2],[5,1]])
    idx = pareto_front_indices_2d(pts)
    assert set(idx.tolist()) == set(range(5))
