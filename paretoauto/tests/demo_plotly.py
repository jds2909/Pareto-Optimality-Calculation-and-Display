# plotly demo with excel linking

import numpy as np
from paretoauto import (sort_fronts, plot_pareto_2d, plot_pareto_3d, load_csv,
                        get_source_rows, save_with_fronts, open_excel_row)

# basic 2D plot
print("\n[2D Demo]")
np.random.seed(42)
points_2d = np.random.random((200, 2))
ranks, fronts, info = sort_fronts(points_2d)
print(f"Algorithm: {info['algo']}, Front 0 size: {len(fronts[0])}")

fig_2d = plot_pareto_2d(points_2d, fronts)
fig_2d.show()

# basic 3D plot
print("\n[3D Demo]")
points_3d = np.random.random((100, 3))
ranks, fronts, info = sort_fronts(points_3d)
print(f"Algorithm: {info['algo']}, Front 0 size: {len(fronts[0])}")

fig_3d = plot_pareto_3d(points_3d, fronts)
fig_3d.show()

# CSV with Excel linking
print("\n[CSV + Excel Linking Demo]")
points, source_info = load_csv('sample_data.csv', ['Cost', 'Time'])
print(f"Loaded {len(points)} products, objectives: {source_info['columns']}")

ranks, fronts, info = sort_fronts(points, directions=['min', 'min'])
print(f"Algorithm: {info['algo']}, Pareto front size: {len(fronts[0])}")

# show pareto optimal products
pareto_products = get_source_rows(fronts[0], source_info)
print("\nPareto-optimal products:")
print(pareto_products.to_string(index=False))

# save with pareto front column
output_file = 'sample_data_with_fronts.csv'
save_with_fronts(source_info, ranks, fronts, output_file)
print(f"\nSaved to: {output_file}")

# interactive plot with hover showing excel rows
fig_csv = plot_pareto_2d(points, fronts, labels=['Cost', 'Time'], source_info=source_info)
fig_csv.show()

# optionally open first pareto point in excel
user_input = input("\nOpen first Pareto point in Excel? (y/n): ").strip().lower()
if user_input in ['y', 'yes']:
    open_excel_row(source_info, fronts[0][0], output_file)
