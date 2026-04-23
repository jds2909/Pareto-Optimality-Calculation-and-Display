import numpy as np
from paretoauto import sort_fronts
from paretoauto.visualise import plot_pareto_2d

np.random.seed(42)
pts = np.random.rand(60, 2) * 10
ranks, fronts, info = sort_fronts(pts, ['min', 'min'])
labels = [f'Solution {i}' for i in range(len(pts))]
fig = plot_pareto_2d(pts, fronts, labels)
fig.show()
