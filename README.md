# Pareto Optimality Calculation and Display

An honours-project Python package for calculating, ranking, and interactively visualising Pareto fronts. It accepts NumPy arrays, CSV files, Excel workbooks, and HiP-HOPS genetic-algorithm output.

The package supports:

- Pareto ranking for minimisation, maximisation, or mixed objectives;
- an automatic 2D sweep-line path and a general non-dominated sorting path;
- interactive 2D and 3D Plotly visualisations;
- animated visualisation of a Pareto front across generations;
- links from plotted points back to their source CSV/Excel rows; and
- direct loading of HiP-HOPS `.xml` and `.js` optimisation results.

## Requirements

- Python 3.9 or newer
- `numpy`
- `pandas`
- `plotly`
- `openpyxl`

The Python package is inside the `paretoauto` directory, so installation commands should be run from there.

## Installation

Clone the repository and install the package in editable mode:

```bash
git clone https://github.com/jds2909/Pareto-Optimality-Calculation-and-Display.git
cd Pareto-Optimality-Calculation-and-Display/paretoauto
python -m pip install -e .
```

Editable installation makes the `paretoauto` command available and means local source-code changes take effect without reinstalling the package.

## Quick start

The following example calculates all Pareto fronts for a two-objective problem in which both objectives are minimised:

```python
import numpy as np

from paretoauto import sort_fronts
from paretoauto.visualise import plot_pareto_2d

points = np.array([
    [1.0, 5.0],
    [2.0, 3.0],
    [3.0, 4.0],
    [4.0, 1.0],
])

ranks, fronts, info = sort_fronts(
    points,
    directions=["min", "min"],
)

print("Ranks:", ranks)
print("Pareto-optimal indices:", fronts[0])
print("Algorithm:", info["algo"])

figure = plot_pareto_2d(
    points,
    fronts,
    labels=["Cost", "Risk"],
)
figure.show()
```

`sort_fronts` returns:

- `ranks`: an array containing the front number for each input row;
- `fronts`: lists of input indices grouped by front, where `fronts[0]` is the Pareto-optimal set; and
- `info`: metadata identifying the selected algorithm and whether it is approximate.

All objectives default to minimisation. To mix directions, pass one direction per objective:

```python
# Minimise cost and maximise reliability.
ranks, fronts, info = sort_fronts(
    points,
    directions=["min", "max"],
)
```

## Loading CSV and Excel data

Use `load_csv` or `load_excel` to retain the source data alongside the objective array:

```python
from paretoauto import get_source_rows, load_csv, save_with_fronts, sort_fronts

points, source_info = load_csv(
    "results.csv",
    objective_columns=["Cost", "Risk"],
)

ranks, fronts, info = sort_fronts(points, directions=["min", "min"])

# Inspect the original rows belonging to the first Pareto front.
pareto_rows = get_source_rows(fronts[0], source_info)
print(pareto_rows)

# Add a Pareto_Front column and write the complete data set.
save_with_fronts(
    source_info,
    ranks,
    fronts,
    "results_with_fronts.csv",
)
```

For an Excel workbook, replace `load_csv` with:

```python
from paretoauto import load_excel

points, source_info = load_excel(
    "results.xlsx",
    sheet_name=0,
    objective_columns=["Cost", "Risk"],
)
```

If `objective_columns` is omitted, all detected numeric columns are used. Input objective values should be numeric and free of missing values.

Pass `source_info` to a plotting function to include source-row details in the hover text:

```python
figure = plot_pareto_2d(
    points,
    fronts,
    labels=["Cost", "Risk"],
    source_info=source_info,
)
figure.write_html("pareto_front.html")
```

Use `plot_pareto_3d` in the same way for three objectives. Plotting functions return standard Plotly `Figure` objects, which can be displayed with `.show()` or saved as standalone HTML with `.write_html(...)`.

## HiP-HOPS output

The command-line interface loads HiP-HOPS optimisation output whose filename begins with `GA_`. Both raw `.xml` files and XML wrapped in a `.js` variable are supported.

View one file directly:

```bash
paretoauto hiphops path/to/GA_model_Generation50_results.xml
```

Choose one or more generations from a directory:

```bash
paretoauto hiphops testHiphop100
```

Animate every generation in a directory:

```bash
paretoauto evolution testHiphop100
```

If no path is supplied, the program attempts to open a folder-selection dialog. Example HiP-HOPS data is included in `testHiphop100`, `testHiphop3D`, and `testHiphopResults`.

HiP-HOPS data can also be loaded from Python:

```python
from paretoauto.io import load_hiphops
from paretoauto.visualise import plot_pareto_2d

points, source_info = load_hiphops("path/to/GA_output.js")

# HiP-HOPS supplies its non-dominated population, so every loaded point is
# displayed as part of front zero.
fronts = [list(range(len(points)))]

figure = plot_pareto_2d(
    points,
    fronts,
    labels=source_info["columns"],
    source_info=source_info,
)
figure.show()
```

## Evolution animation

`plot_evolution_animation` accepts a list of `(generation, points, source_info)` tuples:

```python
from paretoauto.visualise import plot_evolution_animation

generations = [
    (0, generation_0_points, None),
    (1, generation_1_points, None),
]

figure = plot_evolution_animation(
    generations,
    labels=["Cost", "Risk"],
)
figure.show()
```

The resulting figure has play/pause controls and a generation slider. Axis ranges remain fixed across frames to make convergence easier to compare.

## Included examples

After installation, run these from the `paretoauto` directory:

```bash
python plot_2d_example.py
python plot_3d_example.py
python plot_evolution_example.py
python examples/quickcheck.py
```

The first three open interactive Plotly figures. `quickcheck.py` performs a small calculation without plotting.

## Tests

Install pytest and run the test suite from the `paretoauto` directory:

```bash
python -m pip install pytest
python -m pytest tests -v
```

The tests cover the 2D sweep, general non-dominated sorting, mixed objective directions, complete front ranking, and animation hover-data mapping.

## Benchmarks

Run the internal benchmarks with:

```bash
python benchmarks/run_bench.py
```

The benchmark script can optionally compare this package with `paretoset` and `pymoo`:

```bash
python -m pip install paretoset pymoo
python benchmarks/run_bench.py
```

## How it works

- For two objectives, `sort_fronts` repeatedly applies a sweep-line algorithm to extract successive fronts. The individual sweep is `O(n log n)` because the points are sorted by the first objective.
- For three or more objectives, it uses pairwise non-dominated sorting in the style used by NSGA-II. This implementation is straightforward and exact, but its `O(n^2)` comparisons make it best suited to small and medium data sets.
- Maximisation objectives are negated internally so that both algorithms can operate as minimisers.

The current 2D sweep uses strict improvement in the second objective. Identical objective vectors are therefore peeled into successive fronts instead of being assigned the same rank; deduplicate identical objective rows first if this case matters to an analysis.

## Project structure

```text
.
|-- README.md                    # Repository overview and instructions
`-- paretoauto/
    |-- pyproject.toml           # Package metadata and dependencies
    |-- paretoauto/
    |   |-- algorithms/
    |   |   |-- pareto2d.py      # Two-objective sweep-line algorithm
    |   |   `-- ndsort.py        # General non-dominated sorting
    |   |-- cli.py               # HiP-HOPS command-line interface
    |   |-- io.py                # CSV, Excel, and HiP-HOPS input/output
    |   |-- selector.py          # Algorithm selection and front ranking
    |   |-- utils.py             # Objective-direction conversion
    |   `-- visualise.py         # Plotly visualisations and animation
    |-- tests/                    # Automated tests and sample tabular data
    |-- benchmarks/               # Timing and comparison scripts
    |-- examples/                 # Small calculation example
    |-- testHiphop100/            # Multi-generation sample output
    |-- testHiphop3D/             # Three-objective sample output
    `-- testHiphopResults/        # Additional HiP-HOPS sample output
```

## Current scope

This is an honours-project implementation intended to demonstrate Pareto-front calculation, data traceability, and interactive visualisation. The general sorting algorithm favours clarity over large-scale performance, and the command-line interface currently targets HiP-HOPS data; CSV and Excel analysis is available through the Python API.
