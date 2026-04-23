# interactive 2d and 3d plotting using plotly

import numpy as np
import plotly.graph_objects as go
import os
import subprocess
import platform


def _build_hover_detail(source_info, point_idx):
    """Build hover text detail based on data source type."""
    if source_info.get('type') == 'hiphops':
        # show individual ID and top-level components
        ind = source_info['individuals'][point_idx]
        text = f"ID: {ind['id']}<br>"

        # show first few components (full list would be too long)
        encoding = ind['encoding']
        top_level = [k for k in encoding.keys() if '.' not in k][:5]
        for comp in top_level:
            text += f"{comp}: {encoding[comp]}<br>"

        if len(top_level) < len([k for k in encoding.keys() if '.' not in k]):
            text += "...<br>"

        return text
    else:
        # csv/excel - show row reference
        excel_row = point_idx + 2
        df = source_info["dataframe"]
        text = ""
        if len(df.columns) > 0:
            identifier = df.iloc[point_idx, 0]
            text += f'Item: {identifier}<br>'
        text += f'Excel Row: {excel_row}<br><i>Click to open in Excel</i>'
        return text


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
            front_indices = list(fronts[highlight_front])

            # sort by first objective so line traces the front properly
            sort_order = np.argsort(front_pts[:, 0])
            front_pts = front_pts[sort_order]
            front_indices = [front_indices[i] for i in sort_order]

            # build hover text with source info
            hover_texts = []
            for idx, point_idx in enumerate(front_indices):
                hover_text = f'<b>Front {highlight_front}</b><br>{labels[0]}: {front_pts[idx, 0]:.3f}<br>{labels[1]}: {front_pts[idx, 1]:.3f}<br>'

                if source_info is not None:
                    hover_text += _build_hover_detail(source_info, point_idx)

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
        title="Interactive Pareto Front Visualisation",
        xaxis_title=labels[0], yaxis_title=labels[1],
        hovermode='closest', width=900, height=700,
        template='plotly_white'
    )

    if source_info is not None:
        if source_info.get('type') == 'hiphops':
            print("\nHover over points to see component configurations")
        else:
            print("\nHover over points to see Excel row numbers")
            print("Use open_excel_row(source_info, row_index) to open in Excel")

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
            mode='markers',
            marker=dict(size=5, opacity=0.7, line=dict(color='black', width=1)),
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
                        mode='markers',
                        marker=dict(size=4, color='gray', opacity=0.3, line=dict(color='darkgray', width=1)),
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
                    hover_text += _build_hover_detail(source_info, point_idx)

                hover_texts.append(hover_text)

            fig.add_trace(go.Scatter3d(
                x=front_pts[:, 0], y=front_pts[:, 1], z=front_pts[:, 2],
                mode='markers',
                marker=dict(size=8, color='red', opacity=0.9, line=dict(color='darkred', width=1)),
                name=f'Pareto Front {highlight_front}',
                customdata=front_indices,
                hovertemplate='%{text}<extra></extra>',
                text=hover_texts
            ))

    fig.update_layout(
        title="3D Pareto Front Visualisation",
        autosize=True,
        scene=dict(
            xaxis_title=labels[0], yaxis_title=labels[1], zaxis_title=labels[2],
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        ),
        template='plotly_white'
    )

    if source_info is not None:
        if source_info.get('type') == 'hiphops':
            print("\nHover over points to see component configurations")
        else:
            print("\nHover shows Excel row numbers. Use open_excel_row() to open file.")

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

        print(f"Opened {filepath}")
        print(f"  go to row {excel_row}")
    except Exception as e:
        print(f"Error: couldn't open: {e}")
        print(f"   manual path: {filepath}, row {excel_row}")


def plot_evolution_animation(generations_data, labels=None, is_3d=False):
    """Animated Plotly figure showing how the Pareto front evolves across generations.

    parameters
    generations_data  list of (gen_number, points_array, source_info) tuples sorted by generation
    labels            list of objective axis labels
    is_3d             True to produce a 3D scatter animation

    returns plotly Figure with play/pause controls and a generation slider
    """
    if not generations_data:
        raise ValueError("No generation data provided")

    n_obj = generations_data[0][1].shape[1]
    if labels is None:
        labels = [f"Objective {i+1}" for i in range(n_obj)]

    # compute global axis bounds for fixed scale across all frames
    all_points = np.vstack([pts for _, pts, _ in generations_data])
    pad = 0.05
    ranges = []
    for col in range(n_obj):
        lo, hi = all_points[:, col].min(), all_points[:, col].max()
        margin = (hi - lo) * pad if hi != lo else 1.0
        ranges.append((lo - margin, hi + margin))

    def _make_trace(points, source_info, gen_num):
        pts = np.asarray(points)
        # sort by first objective so the line traces the front properly (2D)
        order = np.argsort(pts[:, 0])
        pts = pts[order]
        orig_indices = order.tolist()  # map sorted positions back to original population indices

        hover_texts = []
        for local_i, orig_i in enumerate(orig_indices):
            ht = f"<b>Gen {gen_num}</b><br>"
            for ax_i, lbl in enumerate(labels):
                ht += f"{lbl}: {pts[local_i, ax_i]:.3f}<br>"
            if source_info is not None:
                ht += _build_hover_detail(source_info, orig_i)
            hover_texts.append(ht)

        if is_3d:
            return go.Scatter3d(
                x=pts[:, 0], y=pts[:, 1], z=pts[:, 2],
                mode='markers',
                marker=dict(size=6, color='red', opacity=0.85, line=dict(color='darkred', width=1)),
                name=f'Gen {gen_num}',
                hovertemplate='%{text}<extra></extra>',
                text=hover_texts,
            )
        else:
            return go.Scatter(
                x=pts[:, 0], y=pts[:, 1],
                mode='markers+lines',
                marker=dict(size=10, color='red', opacity=0.9),
                line=dict(color='red', width=2),
                name=f'Gen {gen_num}',
                hovertemplate='%{text}<extra></extra>',
                text=hover_texts,
            )

    # build frames — one per generation
    frames = []
    for gen_num, pts, src_info in generations_data:
        trace = _make_trace(pts, src_info, gen_num)
        frames.append(go.Frame(data=[trace], name=str(gen_num)))

    # initial trace is the first generation
    first_gen, first_pts, first_src = generations_data[0]
    fig = go.Figure(
        data=[_make_trace(first_pts, first_src, first_gen)],
        frames=frames,
    )

    # slider steps — one per generation
    slider_steps = [
        dict(
            args=[[str(gen_num)], dict(frame=dict(duration=200, redraw=True), mode='immediate')],
            label=f"Gen {gen_num}",
            method='animate',
        )
        for gen_num, _, _ in generations_data
    ]

    # play / pause buttons
    updatemenus = [dict(
        type='buttons',
        showactive=False,
        y=0,
        x=0.1,
        xanchor='right',
        yanchor='top',
        buttons=[
            dict(label='Play', method='animate',
                 args=[None, dict(frame=dict(duration=200, redraw=True),
                                  fromcurrent=True, mode='immediate')]),
            dict(label='Pause', method='animate',
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode='immediate')]),
        ]
    )]

    sliders = [dict(
        active=0,
        steps=slider_steps,
        x=0.1, y=0,
        len=0.9,
        xanchor='left', yanchor='top',
        pad=dict(b=10, t=50),
        currentvalue=dict(prefix='Generation: ', visible=True, xanchor='right'),
        transition=dict(duration=100),
    )]

    if is_3d:
        fig.update_layout(
            title="HiP-HOPS Pareto Front Evolution (3D)",
            autosize=True,
            scene=dict(
                xaxis=dict(title=labels[0], range=list(ranges[0])),
                yaxis=dict(title=labels[1], range=list(ranges[1])),
                zaxis=dict(title=labels[2], range=list(ranges[2])),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            ),
            updatemenus=updatemenus,
            sliders=sliders,
            template='plotly_white',
        )
    else:
        fig.update_layout(
            title="HiP-HOPS Pareto Front Evolution",
            xaxis=dict(title=labels[0], range=list(ranges[0])),
            yaxis=dict(title=labels[1], range=list(ranges[1])),
            updatemenus=updatemenus,
            sliders=sliders,
            hovermode='closest',
            width=950, height=750,
            template='plotly_white',
        )

    print(f"\nEvolution animation ready: {len(generations_data)} generation(s)")
    print("Use the Play button or drag the slider to step through generations.")
    return fig


def create_interactive_plot_with_excel_link(points, fronts, source_info, labels=None,
                                            highlight_front=0, is_3d=False, save_with_fronts_path=None):
    # convenience function that creates plot and prints usage tips
    if is_3d:
        fig = plot_pareto_3d(points, fronts, labels, highlight_front, True, source_info)
    else:
        fig = plot_pareto_2d(points, fronts, labels, highlight_front, True, source_info)

    print("\n" + "="*60)
    print("Interactive Pareto Visualisation")
    print("="*60)
    if source_info.get('type') == 'hiphops':
        print("hover to see component configurations")
    else:
        print("hover to see excel row numbers")
        print(f"example: open_excel_row(source_info, {fronts[highlight_front][0]})")
    print("="*60 + "\n")

    return fig
