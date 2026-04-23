import numpy as np
from paretoauto.visualise import plot_evolution_animation

np.random.seed(42)

# simulate 8 generations of a GA converging toward the Pareto front
generations_data = []
for gen in range(8):
    n_pts = 30
    # population gradually converges: spread shrinks, front improves each gen
    spread = 10 - gen * 0.8
    offset = gen * 0.3
    pts = np.random.rand(n_pts, 2) * spread + offset
    source_info = None
    generations_data.append((gen, pts, source_info))

fig = plot_evolution_animation(generations_data, labels=['Objective 1', 'Objective 2'])
fig.show()
