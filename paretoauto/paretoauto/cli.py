# command line interface for paretoauto

import argparse
import os
import glob

from .io import load_hiphops
from .visualise import plot_pareto_2d


def pick_folder():
    """Open a folder picker dialog. Returns path or None if cancelled."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()  # hide the main window
        folder = filedialog.askdirectory(title="Select folder containing HiP-HOPS output files")
        root.destroy()
        return folder if folder else None
    except Exception as e:
        print(f"Could not open file picker: {e}")
        return None


def find_hiphops_files(folder):
    """Find all HiP-HOPS output files in a folder, sorted by generation."""
    patterns = ['*.xml', '*.js']
    files = []

    for pattern in patterns:
        files.extend(glob.glob(os.path.join(folder, f'GA_*{pattern}')))

    # remove duplicates (same generation might have both .xml and .js)
    # prefer .xml over .js if both exist
    seen_gens = {}
    for f in files:
        # extract generation number from filename
        basename = os.path.basename(f)
        if 'Generation' in basename:
            try:
                gen_part = basename.split('Generation')[1]
                gen_num = int(gen_part.split('_')[0])

                # prefer .xml over .js
                if gen_num not in seen_gens or f.endswith('.xml'):
                    seen_gens[gen_num] = f
            except (IndexError, ValueError):
                continue

    # sort by generation number
    sorted_files = sorted(seen_gens.items(), key=lambda x: x[0])
    return [f for _, f in sorted_files]


def cmd_hiphops(args):
    """Handle the hiphops visualisation command."""
    path = args.path

    # if no path given, open file picker
    if not path:
        print("No path specified, opening folder picker...")
        path = pick_folder()
        if not path:
            print("No folder selected, exiting.")
            return

    # check if path exists
    if not os.path.exists(path):
        print(f"Path not found: {path}")
        return

    # if it's a file, load just that file
    if os.path.isfile(path):
        files = [path]
    else:
        # it's a folder, find all hiphops files
        files = find_hiphops_files(path)
        if not files:
            print(f"No HiP-HOPS output files found in: {path}")
            return

    print(f"\nFound {len(files)} file(s):")
    for i, f in enumerate(files, 1):
        # extract generation number for cleaner display
        basename = os.path.basename(f)
        if 'Generation' in basename:
            gen_part = basename.split('Generation')[1].split('_')[0]
            print(f"  {i}. Generation {gen_part}")
        else:
            print(f"  {i}. {basename}")

    # get user selection
    if len(files) == 1:
        selected = [0]
    else:
        print("\nEnter number(s) to visualise (comma-separated, or 'all'):")
        choice = input("> ").strip()

        if choice.lower() == 'all':
            selected = list(range(len(files)))
        else:
            try:
                selected = [int(x.strip()) - 1 for x in choice.split(',')]
                # validate
                for s in selected:
                    if s < 0 or s >= len(files):
                        print(f"Invalid selection: {s + 1}")
                        return
            except ValueError:
                print("Invalid input. Use numbers separated by commas.")
                return

    # load and plot selected files
    for idx in selected:
        filepath = files[idx]
        print(f"\nLoading: {os.path.basename(filepath)}")

        points, source_info = load_hiphops(filepath)

        print(f"  Model: {source_info['model']}")
        print(f"  Generation: {source_info['generation']}")
        print(f"  Objectives: {source_info['columns']}")
        print(f"  Solutions: {len(points)}")

        # plot
        fronts = [list(range(len(points)))]
        labels = source_info['columns']

        fig = plot_pareto_2d(points, fronts, labels, source_info=source_info)
        fig.update_layout(
            title=f"HiP-HOPS Pareto Front - {source_info['model']} (Gen {source_info['generation']})"
        )
        fig.show()


def main():
    parser = argparse.ArgumentParser(
        prog='paretoauto',
        description='Pareto front visualisation and analysis tools'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # hiphops command
    hiphops_parser = subparsers.add_parser(
        'hiphops',
        help='Visualise HiP-HOPS optimisation output'
    )
    hiphops_parser.add_argument(
        'path',
        nargs='?',
        default=None,
        help='Path to file or folder containing HiP-HOPS output (opens picker if not specified)'
    )
    hiphops_parser.set_defaults(func=cmd_hiphops)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    args.func(args)


if __name__ == '__main__':
    main()
