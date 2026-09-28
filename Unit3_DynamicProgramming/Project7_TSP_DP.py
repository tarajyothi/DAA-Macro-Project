"""
DAA Macro Project - Unit III : Dynamic Programming
Project 7 : Traveling Salesperson Problem (Held-Karp subset DP), 4 cities

State      : dp[S][j] = minimum cost of a path that starts at city A (index 0),
             visits EXACTLY the cities in subset S (a subset of {B, C, D}) and
             ends at city j, where j is in S.
Base case  : dp[{j}][j] = dist[A][j]
Transition : dp[S][j] = min over k in S - {j} of  dp[S - {j}][k] + dist[k][j]
Answer     : min over j of  dp[all][j] + dist[j][A]

Subsets are stored as bit masks over the cities B, C, D
(bit 0 -> B, bit 1 -> C, bit 2 -> D).

Run: python Project7_TSP_DP.py
Complexity: time O(n^2 * 2^n), space O(n * 2^n)
"""
from itertools import combinations

CITIES = ["A", "B", "C", "D"]
DIST = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]
INF = float("inf")


def subset_name(mask, n=len(CITIES)):
    """Bit i of the mask stands for city i+1 (city 0 = A is the start)."""
    return "{" + ",".join(CITIES[i + 1] for i in range(n - 1) if mask >> i & 1) + "}"


def held_karp(dist=DIST):
    n = len(dist)
    m = n - 1                                   # cities other than the start
    full = (1 << m) - 1
    dp = {}                                     # (mask, j) -> cost   (j is 0-based among B..D)
    parent = {}                                 # (mask, j) -> previous city (None for base states)
    transitions = []                            # (from_state, to_state, edge_cost, candidate_cost)

    for j in range(m):                          # base states: A -> j
        dp[(1 << j, j)] = dist[0][j + 1]
        parent[(1 << j, j)] = None

    # iterate subsets in increasing size so every predecessor is already computed
    for size in range(2, m + 1):
        for combo in combinations(range(m), size):
            mask = sum(1 << c for c in combo)
            for j in combo:
                prev_mask = mask ^ (1 << j)
                best, best_k = INF, None
                for k in combo:
                    if k == j:
                        continue
                    cand = dp[(prev_mask, k)] + dist[k + 1][j + 1]
                    transitions.append(((prev_mask, k), (mask, j), dist[k + 1][j + 1], cand))
                    if cand < best:
                        best, best_k = cand, k
                dp[(mask, j)] = best
                parent[(mask, j)] = best_k

    # close the tour: last city -> A.  Ties are broken toward the later city.
    best_cost, last = INF, None
    for j in range(m):
        total = dp[(full, j)] + dist[j + 1][0]
        if total <= best_cost:
            best_cost, last = total, j

    # reconstruct the route by following parent pointers backwards
    route, mask, j = [], full, last
    while j is not None:
        route.append(j + 1)
        pj = parent[(mask, j)]
        mask ^= 1 << j
        j = pj
    route = [0] + route[::-1] + [0]
    return dp, parent, transitions, best_cost, last, route


def main():
    dp, parent, transitions, best_cost, last, route = held_karp()
    m = len(CITIES) - 1
    full = (1 << m) - 1

    print("=== TSP with Dynamic Programming (Held-Karp), 4 cities ===\n")
    print("Distance matrix:")
    print("     " + "  ".join(f"{c:>3}" for c in CITIES))
    for i, row in enumerate(DIST):
        print(f"  {CITIES[i]}  " + "  ".join(f"{d:>3}" for d in row))

    print("\nDP states  dp[S][j]  (path starts at A, visits set S, ends at j):")
    for size in range(1, m + 1):
        for combo in combinations(range(m), size):
            mask = sum(1 << c for c in combo)
            cells = ", ".join(f"end {CITIES[j+1]}: {dp[(mask, j)]}" for j in combo)
            print(f"  S={subset_name(mask):<9} | {cells}")

    print(f"\nState transitions ({len(transitions)} total):")
    for (pm, pj), (nm, nj), w, cand in transitions:
        print(f"  dp[{subset_name(pm)},{CITIES[pj+1]}]={dp[(pm, pj)]}  +  d({CITIES[pj+1]},{CITIES[nj+1]})={w}"
              f"  ->  candidate for dp[{subset_name(nm)},{CITIES[nj+1]}] = {cand}")

    print("\nClosing the tour (return to A):")
    for j in range(m):
        print(f"  dp[{subset_name(full)},{CITIES[j+1]}] + d({CITIES[j+1]},A) = "
              f"{dp[(full, j)]} + {DIST[j+1][0]} = {dp[(full, j)] + DIST[j+1][0]}")

    print("\nOptimal tour :", " -> ".join(CITIES[i] for i in route))
    print("Minimum cost :", best_cost)
    print("(The reverse tour has the same cost; both describe the same cycle.)")


if __name__ == "__main__":
    main()
