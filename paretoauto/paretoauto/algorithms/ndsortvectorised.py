# loop based nondominated sorting (minimisation) obj >= 2
# basic and not optimised for now, good for small/medium num of points.

import numpy as np

def dominates_pair(a, b):
    return np.all(a <= b) and np.any(a < b)

def non_dominated_sort(points):
    P = np.asarray(points)
    N = len(P)
    dom_cnt = np.zeros(N, dtype=int)
    dominates_list = [[] for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            if dominates_pair(P[i], P[j]):
                dominates_list[i].append(j)
            elif dominates_pair(P[j], P[i]):
                dom_cnt[i] += 1

    ranks = -np.ones(N, dtype=int)
    fronts = []
    current = [i for i in range(N) if dom_cnt[i] == 0]
    r = 0
    while current:
        fronts.append(current)
        for i in current:
            ranks[i] = r
        next_front = []
        for i in current:
            for j in dominates_list[i]:
                dom_cnt[j] -= 1
                if dom_cnt[j] == 0:
                    next_front.append(j)
        current = next_front
        r += 1
    return ranks, fronts
