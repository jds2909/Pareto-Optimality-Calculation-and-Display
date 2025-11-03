import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# check if poitn is dominated by any opther point
def is_dominated(point, others):
    for other in others:
        if all(other <= point) and any(other < point):
            return True
    return False

# identify non dominated points in dataset
# array of shape as parameter
# returns array of pareto optimal points
def pareto_frontier(points):
    pareto_points = []
    for i, p in enumerate(points):
        others = np.delete(points, i, axis=0)
        if not is_dominated(p, others):
            pareto_points.append(p)
    return np.array(pareto_points)


if __name__ == "__main__":
    # generate random data
    np.random.seed(0)
    data = np.random.rand(30, 2) * 10  # 30 points & 2 objectives

    # calculate pareto frontier
    pareto_points = pareto_frontier(data)

    # static 2d plot matplotlib
    plt.figure(figsize=(6, 5))
    plt.scatter(data[:, 0], data[:, 1], label="All Points", alpha=0.5)
    plt.scatter(pareto_points[:, 0], pareto_points[:, 1], color="red", label="Pareto Front")
    plt.xlabel("Objective 1")
    plt.ylabel("Objective 2")
    plt.title("Pareto Front 2D - Static View")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # interactive 2d plot using plotly
    df = {
        "Objective 1": data[:, 0],
        "Objective 2": data[:, 1],
        "Type": ["Pareto" if any((data[i] == p).all() for p in pareto_points) else "Other"
                 for i in range(len(data))]
    }

    fig = px.scatter(
        df,
        x="Objective 1",
        y="Objective 2",
        color="Type",
        title="Pareto Front 2D - Interactive View",
        color_discrete_map={"Pareto": "red", "Other": "blue"},
        symbol="Type"
    )
    fig.update_traces(marker=dict(size=10, opacity=0.8))
    fig.show()