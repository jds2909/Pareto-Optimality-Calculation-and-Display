# package init: exports main functions

from .selector import sort_fronts
from .utils import apply_directions
from .algorithms.pareto2d import pareto_front_indices_2d
from .algorithms.ndsort import non_dominated_sort
from .io import load_csv, load_excel, get_source_rows, save_with_fronts, print_row_references
from .visualise import plot_pareto_2d, plot_pareto_3d, open_excel_row, create_interactive_plot_with_excel_link

__version__ = "0.1.0"