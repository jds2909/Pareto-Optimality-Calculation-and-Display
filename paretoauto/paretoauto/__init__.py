# package init: exports main functions

from .selector import sort_fronts
from .utils import apply_directions
from .algorithms.pareto2d import pareto_front_indices_2d
from .algorithms.ndsort import non_dominated_sort
from .io import load_csv, load_excel, get_source_rows
from .visualise import plot_pareto_2d, plot_pareto_3d

__version__ = "0.1.0"