"""Tests for plot_evolution_animation hover index correctness."""

import numpy as np
import pytest
from paretoauto.visualise import plot_evolution_animation


def _make_hiphops_source(individuals):
    """Build a minimal hiphops-style source_info for testing."""
    return {
        'type': 'hiphops',
        'individuals': individuals,
    }


def _individuals(n):
    """Create n individuals with distinct IDs and single top-level component."""
    return [
        {'id': f'IND_{i}', 'objectives': {}, 'encoding': {f'Comp_{i}': f'Impl_{i}'}}
        for i in range(n)
    ]


def _get_hover_texts(fig, frame_index=0):
    """Extract hover text list from a figure frame."""
    return list(fig.frames[frame_index].data[0].text)


# ---------------------------------------------------------------------------
# Core regression: sorted position i must show individual at original index
# ---------------------------------------------------------------------------

def test_hover_matches_original_index_after_sort():
    """Regression for the orig_indices bug.

    Points are given in reverse x order so argsort reverses them.
    After sorting, position 0 = original index 2, position 1 = 1, position 2 = 0.
    Each hover text must reference the individual at the *original* index, not the
    sorted position.
    """
    # Reverse x-order: point at index 0 has highest x, index 2 has lowest
    pts = np.array([[3.0, 1.0], [2.0, 2.0], [1.0, 3.0]])
    inds = _individuals(3)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)
    hover = _get_hover_texts(fig)

    # after argsort([3,2,1]) → order=[2,1,0]
    # sorted position 0 → original index 2 → IND_2
    # sorted position 1 → original index 1 → IND_1
    # sorted position 2 → original index 0 → IND_0
    assert 'IND_2' in hover[0], f"position 0 should show IND_2, got: {hover[0]}"
    assert 'IND_1' in hover[1], f"position 1 should show IND_1, got: {hover[1]}"
    assert 'IND_0' in hover[2], f"position 2 should show IND_0, got: {hover[2]}"


def test_hover_correct_when_already_sorted():
    """When points are already sorted by x, sorted pos i == original index i."""
    pts = np.array([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]])
    inds = _individuals(3)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)
    hover = _get_hover_texts(fig)

    assert 'IND_0' in hover[0]
    assert 'IND_1' in hover[1]
    assert 'IND_2' in hover[2]


def test_hover_with_arbitrary_sort_order():
    """Scrambled x order — verify each hover maps to the right individual."""
    # x values: index 1 smallest, index 3 next, index 0 next, index 2 largest
    pts = np.array([[3.0, 1.0], [1.0, 4.0], [4.0, 0.5], [2.0, 2.0]])
    inds = _individuals(4)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)
    hover = _get_hover_texts(fig)

    # argsort([3,1,4,2]) → [1,3,0,2]
    expected_order = [1, 3, 0, 2]
    for sorted_pos, orig_idx in enumerate(expected_order):
        assert f'IND_{orig_idx}' in hover[sorted_pos], (
            f"sorted pos {sorted_pos}: expected IND_{orig_idx}, got: {hover[sorted_pos]}"
        )


def test_hover_x_values_match_sorted_objectives():
    """The x-coordinate shown in hover text must match the point at that sorted position."""
    pts = np.array([[5.0, 1.0], [1.0, 5.0], [3.0, 3.0]])
    inds = _individuals(3)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["Cost", "Risk"], is_3d=False)
    hover = _get_hover_texts(fig)

    # after sort by x: [1.0,5.0], [3.0,3.0], [5.0,1.0]
    assert 'Cost: 1.000' in hover[0]
    assert 'Cost: 3.000' in hover[1]
    assert 'Cost: 5.000' in hover[2]


# ---------------------------------------------------------------------------
# Multi-generation: each frame must independently map its own population
# ---------------------------------------------------------------------------

def test_multi_generation_hover_independent():
    """Each generation frame uses its own population order, not gen 0's."""
    # gen 0: ascending x → order [0,1,2]
    pts0 = np.array([[1.0, 3.0], [2.0, 2.0], [3.0, 1.0]])
    inds0 = _individuals(3)

    # gen 1: descending x → order [2,1,0]
    pts1 = np.array([[3.0, 1.0], [2.0, 2.0], [1.0, 3.0]])
    inds1 = [
        {'id': 'G1_0', 'objectives': {}, 'encoding': {'C': 'G1_0'}},
        {'id': 'G1_1', 'objectives': {}, 'encoding': {'C': 'G1_1'}},
        {'id': 'G1_2', 'objectives': {}, 'encoding': {'C': 'G1_2'}},
    ]

    generations_data = [
        (0, pts0, _make_hiphops_source(inds0)),
        (1, pts1, _make_hiphops_source(inds1)),
    ]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)

    hover_gen0 = _get_hover_texts(fig, frame_index=0)
    hover_gen1 = _get_hover_texts(fig, frame_index=1)

    # gen 0 sorted pos 0 → original 0
    assert 'IND_0' in hover_gen0[0]

    # gen 1 sorted pos 0 → original 2 (smallest x=1.0 is at index 2 of pts1)
    assert 'G1_2' in hover_gen1[0]
    assert 'G1_1' in hover_gen1[1]
    assert 'G1_0' in hover_gen1[2]


# ---------------------------------------------------------------------------
# 3D path: no x-sort applied, so positions are identity — just check structure
# ---------------------------------------------------------------------------

def test_3d_hover_contains_individual_ids():
    """3D traces don't sort, so sorted pos i == original index i."""
    pts = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    inds = _individuals(3)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y", "Z"], is_3d=True)
    hover = _get_hover_texts(fig)

    for i in range(3):
        assert f'IND_{i}' in hover[i], f"3D hover pos {i} should show IND_{i}"


# ---------------------------------------------------------------------------
# Structural sanity checks
# ---------------------------------------------------------------------------

def test_frame_count_matches_generations():
    pts = np.array([[1.0, 2.0], [3.0, 1.0]])
    inds = _individuals(2)
    src = _make_hiphops_source(inds)
    generations_data = [(i, pts, src) for i in range(5)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)
    assert len(fig.frames) == 5


def test_hover_count_matches_point_count():
    pts = np.random.default_rng(0).random((10, 2))
    inds = _individuals(10)
    src = _make_hiphops_source(inds)
    generations_data = [(0, pts, src)]

    fig = plot_evolution_animation(generations_data, labels=["X", "Y"], is_3d=False)
    hover = _get_hover_texts(fig)
    assert len(hover) == 10
