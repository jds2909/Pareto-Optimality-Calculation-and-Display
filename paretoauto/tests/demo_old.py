import numpy as np
import matplotlib.pyplot as plt
from paretoauto import sort_fronts, plot_pareto_2d, plot_pareto_3d, load_csv, get_source_rows, save_with_fronts, print_row_references

# 2D demo
print("2D Demo")
np.random.seed(42)
points_2d = np.random.random((200, 2))
ranks, fronts, info = sort_fronts(points_2d)
print(f"Algorithm used: {info['algo']}")
print(f"Pareto front size: {len(fronts[0])} points")

fig, ax = plot_pareto_2d(points_2d, fronts)
plt.savefig('pareto_2d.png')
plt.show()

# 3D demo
print("\n3D Demo")
points_3d = np.random.random((100, 3))
ranks, fronts, info = sort_fronts(points_3d)
print(f"Algorithm used: {info['algo']}")
print(f"Pareto front size: {len(fronts[0])} points")

fig, ax = plot_pareto_3d(points_3d, fronts)
plt.savefig('pareto_3d.png')
plt.show()

# CSV Loading Demo
print("\n" + "="*50)
print("CSV Loading Demo - Link back to source rows")
print("="*50)

# Load data from CSV
points, source_info = load_csv('sample_data.csv', objective_columns=['Cost', 'Time'])
print(f"\nLoaded {len(points)} products from CSV")
print(f"Optimizing objectives: {source_info['columns']}")
print(f"Directions: minimize Cost, minimize Time")

# Compute Pareto fronts (assuming we want to minimize both Cost and Time)
ranks, fronts, info = sort_fronts(points, directions=['min', 'min'])
print(f"\nAlgorithm used: {info['algo']}")
print(f"Pareto front (front 0) size: {len(fronts[0])} products")

# Get the original rows for Pareto-optimal products
pareto_products = get_source_rows(fronts[0], source_info)
print(f"\nPareto-optimal products:")
print(pareto_products.to_string(index=False))

# Show all fronts
print(f"\nTotal fronts found: {len(fronts)}")
for i, front in enumerate(fronts):
    print(f"  Front {i}: {len(front)} products")

# Print Excel row references for Pareto-optimal products
print_row_references(fronts[0], source_info, front_number=0)

# Save results to a new file with Pareto_Front column
output_file = 'sample_data_with_fronts.csv'
result_df = save_with_fronts(source_info, ranks, fronts, output_file)
print(f"\nSaved results to: {output_file}")
print(f"You can now open this file in Excel and filter by 'Pareto_Front' column")
print(f"  - Front 0 = Pareto optimal (best)")
print(f"  - Front 1 = Second best")
print(f"  - etc.")

# Ask user if they want to open the file in Excel
import os
import subprocess
import platform

user_input = input("\nWould you like to open this file in Excel? (y/n): ").strip().lower()
if user_input in ['y', 'yes']:
    try:
        # Get absolute path to the file
        abs_path = os.path.abspath(output_file)

        # Open file based on operating system
        if platform.system() == 'Windows':
            os.startfile(abs_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', abs_path])
        else:  # Linux
            subprocess.run(['xdg-open', abs_path])

        print(f"Opening {output_file} in Excel...")
    except Exception as e:
        print(f"Could not open file automatically: {e}")
        print(f"Please open manually: {os.path.abspath(output_file)}")
else:
    print("Skipping file open.")