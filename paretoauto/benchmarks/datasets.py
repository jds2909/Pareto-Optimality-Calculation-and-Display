# synthetic dataset generators for testing

import numpy as np


def generate_random_uniform(n_points, n_objectives, seed=None):
    # generate random points uniformly in [0, 1]
    if seed is not None:
        np.random.seed(seed)
    return np.random.random((n_points, n_objectives))


def generate_cloud(n_points, n_objectives, center=0.5, spread=0.2, seed=None):
    # generate points in gaussian cloud
    if seed is not None:
        np.random.seed(seed)
    return np.random.normal(center, spread, (n_points, n_objectives))


def generate_pareto_front_2d(n_points, front_type='convex', seed=None):
    # generate 2D points with known pareto front shape
    if seed is not None:
        np.random.seed(seed)

    # 1/3 on front & 2/3 dominated
    n_front = n_points // 3
    n_dominated = n_points - n_front

    t = np.linspace(0, 1, n_front)

    if front_type == 'convex':
        front_x = t
        front_y = (1 - t**2)**0.5
    elif front_type == 'concave':
        front_x = t**2
        front_y = (1 - t)**2
    else:  # linear
        front_x = t
        front_y = 1 - t

    front_points = np.column_stack([front_x, front_y])

    # dominated points behind front
    dominated = np.random.random((n_dominated, 2))
    dominated = dominated * 0.8 + 0.2

    return np.vstack([front_points, dominated])


def generate_dtlz1(n_points, n_objectives, seed=None):
    # generate points similar to DTLZ1 test problem
    if seed is not None:
        np.random.seed(seed)

    points = np.random.random((n_points, n_objectives))

    # normalise to simplex
    row_sums = points.sum(axis=1, keepdims=True)
    points = points / row_sums

    # add noise for dominated solutions
    noise = np.random.random((n_points, n_objectives)) * 0.3
    points = points + noise

    return points


def generate_scaled(n_points, n_objectives, seed=None):
    # generate points w/ different scales per objective
    if seed is not None:
        np.random.seed(seed)

    scales = [10**i for i in range(n_objectives)]
    points = np.random.random((n_points, n_objectives))
    return points * np.array(scales)