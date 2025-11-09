# quick check for algorithms (no plotting)
import numpy as np
from paretoauto.algorithms.pareto2d import pareto_front_indices_2d
from paretoauto.algorithms.ndsort import non_dominated_sort

if __name__ == "__main__":
    np.random.seed(0)
    data2 = np.random.rand(20, 2) * 10
    f0 = pareto_front_indices_2d(data2)
    print("2D: front0 size:", len(f0))

    data3 = np.random.rand(30, 3) * 10
    ranks, fronts = non_dominated_sort(data3)
    print("3D: front0 size:", len(fronts[0]))
