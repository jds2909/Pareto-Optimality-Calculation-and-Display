# demo loading and visualising hiphops optimisation output

import sys
import os
sys.path.insert(0, '..')

from paretoauto.io import load_hiphops
from paretoauto.visualise import plot_pareto_2d

# paths relative to paretoauto folder
base = os.path.join(os.path.dirname(__file__), '..', 'testHiphopResults')

# test with generation 50 (.xml file)
print("Loading Generation 50 (xml)...")
points_50, info_50 = load_hiphops(
    os.path.join(base, 'GA_tutorial6_optimisation_Analysis_Generation50_PopulationVariable56_ChildPopulationSize100_Archive_TreeEncoding_RunNumber1.xml')
)
print(f"  Model: {info_50['model']}")
print(f"  Generation: {info_50['generation']}")
print(f"  Objectives: {info_50['columns']}")
print(f"  Solutions: {len(points_50)}")

# test with generation 100 (.js file)
print("\nLoading Generation 100 (js)...")
points_100, info_100 = load_hiphops(
    os.path.join(base, 'GA_tutorial6_optimisation_Analysis_Generation100_PopulationVariable56_ChildPopulationSize100_Archive_TreeEncoding_RunNumber1.js')
)
print(f"  Model: {info_100['model']}")
print(f"  Generation: {info_100['generation']}")
print(f"  Solutions: {len(points_100)}")

# plot generation 50
# hiphops output is already the pareto front, so fronts = all indices
fronts_50 = [list(range(len(points_50)))]
labels = info_50['columns']

fig = plot_pareto_2d(points_50, fronts_50, labels, source_info=info_50)
fig.update_layout(title=f"HiP-HOPS Pareto Front - {info_50['model']} (Gen {info_50['generation']})")
fig.show()
