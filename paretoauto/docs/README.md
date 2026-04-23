# paretoauto

A Python package for computing and visualising Pareto fronts, built as part of my final year project at the University of Hull.

The main idea is that you give it a set of solutions with multiple objective values (cost, risk, weight, whatever) and it works out which solutions are Pareto-optimal — i.e. you can't improve one objective without making another worse. It then visualises the results interactively using Plotly, and has specific support for loading HiP-HOPS genetic algorithm output files.

---

## Setup

You'll need Python 3.9+ and the following packages:

```
pip install .
```

That installs everything from `pyproject.toml` (numpy, pandas, plotly, openpyxl) and also registers the `paretoauto` command so you can run it from the terminal.

If you want to run the benchmarks against external libraries:

```
pip install paretoset pymoo
```

---

## Quickstart

The simplest use case — give it a numpy array and it handles the rest:

```python
import numpy as np
from paretoauto import sort_fronts
from paretoauto.visualise import plot_pareto_2d

pts = np.random.rand(60, 2) * 10
ranks, fronts, info = sort_fronts(pts, directions=['min', 'min'])

print(f"Algorithm: {info['algo']}")
print(f"Pareto front has {len(fronts[0])} solutions")

fig = plot_pareto_2d(pts, fronts)
fig.show()  # opens in browser
```

There are also three ready-to-run example scripts in the project root:

```
python plot_2d_example.py
python plot_3d_example.py
python plot_evolution_example.py
```

---

## How sort_fronts works

```python
ranks, fronts, info = sort_fronts(points, directions=None)
```

`points` is an (n, m) array — n solutions, m objectives. `directions` is a list like `['min', 'max', 'min']` telling it which objectives to minimise and which to maximise. If you leave it out, everything defaults to minimise.

It returns three things:
- `ranks` — a 1D array where `ranks[i]` tells you which front solution `i` is on. Rank 0 means Pareto-optimal.
- `fronts` — a list of lists, where `fronts[0]` contains the indices of all Pareto-optimal solutions, `fronts[1]` the next layer, and so on.
- `info` — a small dict with `algo` (which algorithm was used) and `approx` (always False, everything here is exact).

The algorithm it picks depends on how many objectives you have:
- **2 objectives**: uses a sweep-line algorithm, O(n log n). Very fast.
- **3+ objectives**: uses non-dominated sort (the NSGA-II approach), O(n²). Correct but slower for large inputs.

Example with mixed directions:

```python
# minimise cost, maximise reliability
ranks, fronts, info = sort_fronts(pts, directions=['min', 'max'])
```

---

## Loading data from files

### CSV or Excel

```python
from paretoauto import load_csv, sort_fronts, save_with_fronts, get_source_rows

points, source_info = load_csv('mydata.csv', objective_columns=['Cost', 'Risk'])
ranks, fronts, info = sort_fronts(points)

# get the actual rows from the dataframe for the Pareto-optimal solutions
pareto_rows = get_source_rows(fronts[0], source_info)
print(pareto_rows)

# save results back to a file with a Pareto_Front column added
save_with_fronts(source_info, ranks, fronts, 'mydata_with_fronts.csv')
```

For Excel it's the same but use `load_excel`:

```python
from paretoauto import load_excel
points, source_info = load_excel('mydata.xlsx', sheet_name=0, objective_columns=['Cost', 'Risk'])
```

If you skip `objective_columns`, it automatically picks all numeric columns.

The `source_info` dict is passed into the plot functions to enable hover details — hovering over a point shows which row it came from in the original file.

---

## Visualisation

All the plot functions return a Plotly `Figure`. Call `.show()` to open it in a browser or `.write_html('out.html')` to save it as a standalone file.

### 2D plot

```python
from paretoauto.visualise import plot_pareto_2d

fig = plot_pareto_2d(
    points,
    fronts,
    labels=['Cost', 'Risk'],
    highlight_front=0,       # the front shown in red
    show_all=True,           # whether to show dominated fronts in grey
    source_info=source_info  # pass this to get hover details
)
fig.show()
```

The highlighted front is drawn with a line connecting points in objective-1 order, so the trade-off curve shape is visible.

### 3D plot

```python
from paretoauto.visualise import plot_pareto_3d

fig = plot_pareto_3d(points, fronts, labels=['Cost', 'Risk', 'Weight'])
fig.show()
```

Fully rotatable. The 3D plot doesn't draw connecting lines since there's no sensible single ordering in 3D.

### Evolution animation

This is for showing how the Pareto front changes across generations of a GA run. You give it a list of `(generation_number, points_array, source_info)` tuples:

```python
from paretoauto.visualise import plot_evolution_animation

generations_data = [
    (0, pts_gen0, src_gen0),
    (1, pts_gen1, src_gen1),
    # etc.
]

fig = plot_evolution_animation(generations_data, labels=['Cost', 'Risk'], is_3d=False)
fig.show()
```

The output has a Play button and a slider so you can scrub through generations manually. Axes are fixed across all frames so you can see the front actually converging.

---

## HiP-HOPS integration

HiP-HOPS outputs its GA results as `.xml` or `.js` files (one per generation, named like `GA_modelname_Generation10_...xml`). The package can parse these directly.

### CLI — view a single generation

```
paretoauto hiphops <path>
```

Pass a folder and it lists all the generation files it finds, then asks which one(s) you want to view. Pass a single file to go straight to the plot. Leave `<path>` out entirely to get a folder picker dialog.

```
paretoauto hiphops testHiphop100
```

Then type a generation number (e.g. `50`) or `all` when prompted.

### CLI — evolution animation across all generations

```
paretoauto evolution <folder>
```

Loads every generation file in the folder and builds the animated plot automatically.

```
paretoauto evolution testHiphop100
```

### Python API

If you want to load HiP-HOPS files in your own script:

```python
from paretoauto.io import load_hiphops
from paretoauto.visualise import plot_pareto_2d

points, source_info = load_hiphops('GA_tutorial6_Generation100.js')

print(source_info['model'])      # model name from the XML
print(source_info['generation']) # generation number
print(source_info['columns'])    # objective names
print(len(points))               # number of solutions in the Pareto front

# HiP-HOPS output is already the Pareto front so all indices are front 0
fronts = [list(range(len(points)))]
fig = plot_pareto_2d(points, fronts, labels=source_info['columns'], source_info=source_info)
fig.show()
```

When you hover over points in the plot, it shows the component configuration for that solution — which implementation was chosen for each top-level system component.

Both `.xml` and `.js` formats are supported. The `.js` files are what HiP-HOPS normally exports — they're just XML wrapped inside a JavaScript variable assignment, so the parser strips the wrapper first.

---

## Tests

```
python -m pytest tests/ -v
```

19 tests total. They cover the core algorithm correctness (2D sweep, non-dominated sort, agreement between the two), direction handling, and the evolution animation hover index mapping. All should pass.

---

## Benchmarks

```
python benchmarks/run_bench.py
```

Times the internal algorithms at various sizes and compares against `paretoset` and `pymoo` if you have them installed. Results are printed to the terminal.

Results from my machine (Windows 11, Python 3.14, mean of 3 runs):

| | n=100 | n=500 | n=1000 | n=2000 |
|---|---|---|---|---|
| **2D sweep (internal)** | 0.04 ms | 0.21 ms | 0.42 ms | 0.85 ms |
| **paretoauto m=2** | 0.41 ms | 4.31 ms | 12.22 ms | 34.91 ms |
| pymoo m=2 | 0.27 ms | 1.43 ms | 5.71 ms | — |
| paretoset m=2 | ~0.02 ms | ~0.02 ms | ~0.03 ms | — |
| **ND sort (internal)** | 34 ms | 867 ms | 3,495 ms | 14,003 ms |
| **paretoauto m=3** | 34 ms | 879 ms | 3,565 ms | 14,100 ms |
| pymoo m=3 | 0.09 ms | 1.67 ms | 7.46 ms | — |
| paretoset m=3 | ~0.04 ms | ~0.06 ms | ~0.11 ms | — |

The 2D path is reasonably competitive. The 3D algorithm is the obvious weak point — it's O(n²) pure Python, so it gets slow quickly compared to the optimised C implementations in pymoo and paretoset. That's a known limitation and the main thing I'd fix in future work.

---

## Project structure

```
paretoauto/
├── paretoauto/               # the actual package
│   ├── __init__.py           # exports everything at the top level
│   ├── selector.py           # picks which algorithm to use
│   ├── utils.py              # apply_directions() flips max→min
│   ├── io.py                 # file loading (CSV, Excel, HiP-HOPS) and saving
│   ├── visualise.py          # all the Plotly stuff
│   ├── cli.py                # command-line entry point
│   └── algorithms/
│       ├── pareto2d.py       # 2D sweep-line, returns front-0 indices
│       └── ndsort.py         # non-dominated sort for 3+ objectives
├── tests/
│   ├── test_2d.py
│   ├── test_ndsort.py
│   ├── test_sort_fronts.py
│   └── test_evolution_hover.py
├── benchmarks/
│   ├── datasets.py
│   └── run_bench.py
├── plot_2d_example.py
├── plot_3d_example.py
├── plot_evolution_example.py
├── testHiphop100/            # 100 generations of HiP-HOPS output (tutorial6)
├── testHiphop3D/             # 3D HiP-HOPS output (fyffe model)
├── requirements.txt
└── pyproject.toml
```
