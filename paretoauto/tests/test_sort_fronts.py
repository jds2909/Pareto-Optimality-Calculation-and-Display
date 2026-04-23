import numpy as np
import pytest
from paretoauto.selector import sort_fronts


# --- helpers ---

def _assert_fronts_cover_all(ranks, fronts, n):
    """Every point must appear in exactly one front and rank must match front index."""
    seen = set()
    for r, front in enumerate(fronts):
        for idx in front:
            assert idx not in seen, f"point {idx} appears in multiple fronts"
            seen.add(idx)
            assert ranks[idx] == r, f"rank mismatch for point {idx}: ranks={ranks[idx]}, front={r}"
    assert seen == set(range(n)), "not all points are assigned to a front"


def _assert_pareto_correctness(points, fronts):
    """No point in front k should be dominated by any point in front k or later."""
    pts = np.asarray(points)
    for r, front in enumerate(fronts):
        for idx in front:
            for earlier_r in range(r):
                for earlier_idx in fronts[earlier_r]:
                    # earlier fronts must not be dominated by points in later fronts
                    a, b = pts[earlier_idx], pts[idx]
                    assert not (np.all(b <= a) and np.any(b < a)), (
                        f"point {idx} (front {r}) dominates point {earlier_idx} (front {earlier_r})"
                    )


# --- 2D tests ---

def test_2d_all_pareto():
    # classic tradeoff line — every point is on front 0
    pts = np.array([[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]], dtype=float)
    ranks, fronts, info = sort_fronts(pts)
    assert info["algo"] == "2d_sweep"
    assert len(fronts) == 1
    assert set(fronts[0]) == set(range(5))
    _assert_fronts_cover_all(ranks, fronts, len(pts))


def test_2d_two_fronts():
    # front 0: (1,1), (2,2) is dominated by (1,1)... let me be explicit
    # (1,4) and (4,1) are front 0; (2,5), (5,2), (3,3) are all dominated
    pts = np.array([
        [1, 4],   # 0 — front 0
        [4, 1],   # 1 — front 0
        [2, 5],   # 2 — dominated by (1,4): front 1
        [5, 2],   # 3 — dominated by (4,1): front 1
        [3, 3],   # 4 — dominated by (1,4) on x? no: (1,4) has y=4>3, x=1<3. not dominated by (1,4).
                  #     dominated by... (1,4) has y=4 > 3, so (1,4) does NOT dominate (3,3).
                  #     (4,1): x=4>3, so doesn't dominate (3,3) either.
                  #     So (3,3) is actually on front 0 too.
    ], dtype=float)
    # Re-check: front 0 = {0,1,4} all non-dominated; front 1 = {2,3}
    ranks, fronts, info = sort_fronts(pts)
    assert info["algo"] == "2d_sweep"
    _assert_fronts_cover_all(ranks, fronts, len(pts))
    _assert_pareto_correctness(pts, fronts)
    assert set(fronts[0]) == {0, 1, 4}
    assert set(fronts[1]) == {2, 3}


def test_2d_clear_three_fronts():
    # Layered: front 0 clearly dominates front 1, which dominates front 2
    pts = np.array([
        [1, 1],   # 0 — front 0 (dominates everything else)
        [2, 2],   # 1 — front 1 (dominated by 0; dominates 2)
        [3, 3],   # 2 — front 2 (dominated by 0 and 1)
    ], dtype=float)
    ranks, fronts, info = sort_fronts(pts)
    assert info["algo"] == "2d_sweep"
    assert len(fronts) == 3
    assert fronts[0] == [0]
    assert fronts[1] == [1]
    assert fronts[2] == [2]
    _assert_fronts_cover_all(ranks, fronts, len(pts))


def test_2d_all_points_covered():
    # random cloud — just verify structural correctness
    rng = np.random.default_rng(42)
    pts = rng.random((50, 2)) * 10
    ranks, fronts, info = sort_fronts(pts)
    assert info["algo"] == "2d_sweep"
    _assert_fronts_cover_all(ranks, fronts, len(pts))
    _assert_pareto_correctness(pts, fronts)


def test_2d_show_all_fronts_nonempty():
    # regression: before the fix, fronts only had 1 entry for 2D data
    pts = np.array([[1, 1], [2, 2], [3, 3]], dtype=float)
    _, fronts, _ = sort_fronts(pts)
    assert len(fronts) == 3, "2D sort_fronts must return all fronts, not just front 0"


def test_2d_matches_ndsort():
    # 2d_sweep and ndsort must agree on ranks for 2D input
    from paretoauto.algorithms.ndsort import non_dominated_sort
    rng = np.random.default_rng(7)
    pts = rng.random((30, 2)) * 10
    ranks_2d, fronts_2d, _ = sort_fronts(pts)
    ranks_nd, fronts_nd = non_dominated_sort(pts)
    np.testing.assert_array_equal(ranks_2d, ranks_nd)


def test_2d_with_max_direction():
    # maximise both => flip signs => same structure
    pts = np.array([[1, 1], [2, 2], [3, 3]], dtype=float)
    ranks, fronts, _ = sort_fronts(pts, directions=["max", "max"])
    # after negation: (-1,-1), (-2,-2), (-3,-3) — (-3,-3) dominates all
    assert fronts[0] == [2]
    assert fronts[1] == [1]
    assert fronts[2] == [0]


# --- 3D / ndsort path ---

def test_3d_all_points_covered():
    rng = np.random.default_rng(99)
    pts = rng.random((40, 3)) * 10
    ranks, fronts, info = sort_fronts(pts)
    assert info["algo"] == "ndsort_loopy"
    _assert_fronts_cover_all(ranks, fronts, len(pts))
    _assert_pareto_correctness(pts, fronts)


def test_3d_single_front():
    # points on a tradeoff surface — none dominate each other
    pts = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=float)
    _, fronts, _ = sort_fronts(pts)
    assert len(fronts) == 1
    assert set(fronts[0]) == {0, 1, 2}
