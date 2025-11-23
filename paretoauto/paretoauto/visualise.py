# 2D and 3D plotting for pareto fronts

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_pareto_2d(points, fronts=None, labels=None, highlight_front=0, show_all=True):
    # plot 2D pareto front w/ highlighted optimal front
    points = np.asarray(points)
    fig, ax = plt.subplots(figsize=(10, 8))

    if labels is None:
        labels = ["Objective 1", "Objective 2"]

    # if no fronts given, just plot all points
    if fronts is None:
        ax.scatter(points[:, 0], points[:, 1], alpha=0.7)
    else:
        # plot other fronts in gray first
        if show_all:
            for i, front in enumerate(fronts):
                if i != highlight_front:
                    front_pts = points[front]
                    ax.scatter(front_pts[:, 0], front_pts[:, 1],
                              alpha=0.3, c='gray', s=20)

        # plot highlighted front in red
        if highlight_front < len(fronts):
            front_pts = points[fronts[highlight_front]]
            ax.scatter(front_pts[:, 0], front_pts[:, 1],
                      c='red', s=50, alpha=0.9,
                      label=f'Pareto Front {highlight_front}')

            # connect front points with line
            if len(front_pts) > 1:
                sorted_idx = np.argsort(front_pts[:, 0])
                sorted_pts = front_pts[sorted_idx]
                ax.plot(sorted_pts[:, 0], sorted_pts[:, 1],
                       'r-', alpha=0.5, linewidth=1)

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_title("Pareto Front Visualisation")
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig, ax


def plot_pareto_3d(points, fronts=None, labels=None, highlight_front=0, show_all=True):
    # plot 3D pareto front w/ rotation support."""
    points = np.asarray(points)
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    if labels is None:
        labels = ["Objective 1", "Objective 2", "Objective 3"]

    # if no fronts given, just plot all points
    if fronts is None:
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], alpha=0.7)
    else:
        # plot other fronts in gray
        if show_all:
            for i, front in enumerate(fronts):
                if i != highlight_front:
                    front_pts = points[front]
                    ax.scatter(front_pts[:, 0], front_pts[:, 1], front_pts[:, 2],
                              alpha=0.2, c='gray', s=15)

        # plot highlighted front in red
        if highlight_front < len(fronts):
            front_pts = points[fronts[highlight_front]]
            ax.scatter(front_pts[:, 0], front_pts[:, 1], front_pts[:, 2],
                      c='red', s=50, alpha=0.9,
                      label=f'Pareto Front {highlight_front}')

    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    ax.set_title("3D Pareto Front Visualisation")
    ax.legend(loc='upper right')

    return fig, ax