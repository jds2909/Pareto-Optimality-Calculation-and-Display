# interactive 2d and 3d plotting using plotly

import numpy as np
import plotly.graph_objects as go
import os
import subprocess
import platform


def plot_pareto_2d(points, fronts=None, labels=None, highlight_front=0, show_all=True, source_info=None):
    # 2d scatter plot with hover showing excel row numbers
    points = np.asarray(points)
    fig = go.Figure()

    if labels is None:
        labels = ["Objective 1", "Objective 2"]

    if fronts is None:
        # no fronts - just plot all points
        fig.add_trace(go.Scatter(
            x=points[:, 0], y=points[:, 1],
            mode='markers', marker=dict(size=8, opacity=0.7),
            name='All Points'
        ))
    else:
        # plot non-highlighted fronts in gray
        if show_all:
            for i, front in enumerate(fronts):
                if i != highlight_front:
                    front_pts = points[front]
                    fig.add_trace(go.Scatter(
                        x=front_pts[:, 0], y=front_pts[:, 1],
                        mode='markers', marker=dict(size=6, color='gray', opacity=0.3),
                        name=f'Front {i}',
                        hovertemplate=f'<b>Front {i}</b><br>{labels[0]}: %{{x:.3f}}<br>{labels[1]}: %{{y:.3f}}<extra></extra>'
                    ))

        # plot highlighted front in red
        if highlight_front < len(fronts):
            front_pts = points[fronts[highlight_front]]
            front_indices = fronts[highlight_front]

            # build hover text with excel row info if we have source data
            hover_texts = []
            for idx, point_idx in enumerate(front_indices):
                hover_text = f'<b>Front {highlight_front}</b><br>{labels[0]}: {front_pts[idx, 0]:.3f}<br>{labels[1]}: {front_pts[idx, 1]:.3f}<br>'

                if source_info is not None:
                    excel_row = point_idx + 2  # +2 for 1-indexing and header
                    df = source_info["dataframe"]
                    if len(df.columns) > 0:
                        identifier = df.iloc[point_idx, 0]
                        hover_text += f'Item: {identifier}<br>'
                    hover_text += f'Excel Row: {excel_row}<br><i>Click to open in Excel</i>'

                hover_texts.append(hover_text)

            fig.add_trace(go.Scatter(
                x=front_pts[:, 0], y=front_pts[:, 1],
                mode='markers+lines',
                marker=dict(size=12, color='red', opacity=0.9),
                line=dict(color='red', width=2),
                name=f'Pareto Front {highlight_front}',
                customdata=front_indices,
                hovertemplate='%{text}<extra></extra>',
                text=hover_texts
            ))

    fig.update_layout(
        title="Interactive Pareto Front Visualization",
        xaxis_title=labels[0], yaxis_title=labels[1],
        hovermode='closest', width=900, height=700,
        template='plotly_white'
    )

    if source_info is not None:
        print("\n💡 Hover over points to see Excel row numbers")
        print("   Use open_excel_row(source_info, row_index) to open in Excel")

    return fig


def plot_pareto_3d(points, fronts=None, labels=None, highlight_front=0, show_all=True, source_info=None):
    # 3d scatter plot with rotation and hover
    points = np.asarray(points)
    fig = go.Figure()

    if labels is None:
        labels = ["Objective 1", "Objective 2", "Objective 3"]

    if fronts is None:
        fig.add_trace(go.Scatter3d(
            x=points[:, 0], y=points[:, 1], z=points[:, 2],
            mode='markers', marker=dict(size=5, opacity=0.7),
            name='All Points'
        ))
    else:
        # other fronts in gray
        if show_all:
            for i, front in enumerate(fronts):
                if i != highlight_front:
                    front_pts = points[front]
                    fig.add_trace(go.Scatter3d(
                        x=front_pts[:, 0], y=front_pts[:, 1], z=front_pts[:, 2],
                        mode='markers', marker=dict(size=4, color='gray', opacity=0.2),
                        name=f'Front {i}',
                        hovertemplate=f'<b>Front {i}</b><br>{labels[0]}: %{{x:.3f}}<br>{labels[1]}: %{{y:.3f}}<br>{labels[2]}: %{{z:.3f}}<extra></extra>'
                    ))

        # highlighted front in red
        if highlight_front < len(fronts):
            front_pts = points[fronts[highlight_front]]
            front_indices = fronts[highlight_front]

            hover_texts = []
            for idx, point_idx in enumerate(front_indices):
                hover_text = f'<b>Front {highlight_front}</b><br>{labels[0]}: {front_pts[idx, 0]:.3f}<br>{labels[1]}: {front_pts[idx, 1]:.3f}<br>{labels[2]}: {front_pts[idx, 2]:.3f}<br>'

                if source_info is not None:
                    excel_row = point_idx + 2
                    df = source_info["dataframe"]
                    if len(df.columns) > 0:
                        identifier = df.iloc[point_idx, 0]
                        hover_text += f'Item: {identifier}<br>'
                    hover_text += f'Excel Row: {excel_row}'

                hover_texts.append(hover_text)

            fig.add_trace(go.Scatter3d(
                x=front_pts[:, 0], y=front_pts[:, 1], z=front_pts[:, 2],
                mode='markers', marker=dict(size=8, color='red', opacity=0.9),
                name=f'Pareto Front {highlight_front}',
                customdata=front_indices,
                hovertemplate='%{text}<extra></extra>',
                text=hover_texts
            ))

    fig.update_layout(
        title="3D Pareto Front Visualization",
        scene=dict(
            xaxis_title=labels[0], yaxis_title=labels[1], zaxis_title=labels[2],
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        width=900, height=700, template='plotly_white'
    )

    if source_info is not None:
        print("\n💡 Hover shows Excel row numbers. Use open_excel_row() to open file.")

    return fig


def open_excel_row(source_info, row_index, save_with_fronts_path=None):
    # opens excel/csv file at a specific row
    # use annotated file if it exists, otherwise original
    if save_with_fronts_path and os.path.exists(save_with_fronts_path):
        filepath = os.path.abspath(save_with_fronts_path)
    else:
        filepath = os.path.abspath(source_info["filepath"])

    excel_row = row_index + 2  # +2 for 1-indexing and header

    try:
        # open based on os
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])

        print(f"✓ opened {filepath}")
        print(f"  go to row {excel_row}")
    except Exception as e:
        print(f"❌ couldn't open: {e}")
        print(f"   manual path: {filepath}, row {excel_row}")


def create_interactive_plot_with_excel_link(points, fronts, source_info, labels=None,
                                            highlight_front=0, is_3d=False, save_with_fronts_path=None):
    # convenience function that creates plot and prints usage tips
    if is_3d:
        fig = plot_pareto_3d(points, fronts, labels, highlight_front, True, source_info)
    else:
        fig = plot_pareto_2d(points, fronts, labels, highlight_front, True, source_info)

    print("\n" + "="*60)
    print("📊 interactive pareto viz")
    print("="*60)
    print("hover to see excel row numbers")
    print(f"example: open_excel_row(source_info, {fronts[highlight_front][0]})")
    print("="*60 + "\n")

    return fig
