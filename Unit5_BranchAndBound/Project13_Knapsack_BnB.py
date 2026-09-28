"""
DAA Macro Project - Unit V : Branch and Bound
Project 13 : 0/1 Knapsack using Branch and Bound (best-first search)

Sample data : weights = [2, 3, 4, 5], values = [40, 50, 65, 70], capacity = 8

Node  : (level, weight, value, bound)
        level  = number of items already decided (include / exclude)
        weight = total weight of the included items
        value  = total value of the included items
        bound  = UPPER BOUND on the best value reachable from this node,
                 computed by filling the remaining capacity greedily with items
                 in decreasing value/weight order and taking a FRACTION of the
                 first item that does not fit (fractional-knapsack relaxation).

Branching : every node has two children -> INCLUDE the next item / EXCLUDE it.
Leaf      : level == n -> a complete include/exclude assignment (candidate solution)
Pruning   : * infeasible  : weight > capacity
            * bound-pruned: bound <= best value found so far (cannot improve)
Search    : best-first - always expand the live node with the largest bound.

Run: python Project13_Knapsack_BnB.py
Complexity: worst case O(2^n) nodes, but pruning usually removes most of them.
"""
import heapq

WEIGHTS = [2, 3, 4, 5]
VALUES = [40, 50, 65, 70]
CAPACITY = 8


class Node:
    def __init__(self, nid, level, weight, value, bound, parent, decision, taken):
        self.id = nid
        self.level = level          # items decided so far (root = 0)
        self.weight = weight
        self.value = value
        self.bound = bound
        self.parent = parent        # parent node id
        self.decision = decision    # "include" / "exclude" / None for root
        self.taken = taken          # tuple of included item indices
        self.status = "live"        # live | expanded | pruned | infeasible | leaf
        self.order = None           # order in which the node was expanded
        self.prune_best = None      # best value known at the moment the node was pruned by its bound

    def __lt__(self, other):        # tie-break for the heap
        return self.id < other.id


def upper_bound(level, weight, value, w, v, cap):
    """Fractional-knapsack bound for the items level..n-1 (items pre-sorted by v/w)."""
    if weight > cap:
        return 0
    bound, total_w = float(value), weight
    for i in range(level, len(w)):
        if total_w + w[i] <= cap:
            total_w += w[i]
            bound += v[i]
        else:
            bound += (cap - total_w) * v[i] / w[i]     # fraction of the item that still fits
            break
    return bound


def knapsack_bnb(weights=WEIGHTS, values=VALUES, cap=CAPACITY):
    n = len(weights)
    # sort items by value/weight ratio (already sorted for the sample, kept for generality)
    order = sorted(range(n), key=lambda i: values[i] / weights[i], reverse=True)
    w = [weights[i] for i in order]
    v = [values[i] for i in order]

    nodes = []
    counter = 0

    def new_node(level, weight, value, parent, decision, taken):
        nonlocal counter
        b = upper_bound(level, weight, value, w, v, cap)
        node = Node(counter, level, weight, value, b, parent, decision, taken)
        counter += 1
        nodes.append(node)
        return node

    root = new_node(0, 0, 0, None, None, ())
    best_value, best_node = 0, root
    best_history = []                                   # (node id, new best value)
    heap = [(-root.bound, root)]
    expansions = 0

    while heap:
        _, node = heapq.heappop(heap)
        if node.bound <= best_value:                    # bound cannot beat the incumbent
            node.status = "pruned"
            node.prune_best = best_value
            continue
        node.status = "expanded"
        expansions += 1
        node.order = expansions
        if node.level == n:
            continue
        # ---- branch 1: INCLUDE item `level` ----
        i = node.level
        inc = new_node(i + 1, node.weight + w[i], node.value + v[i], node.id, "include",
                       node.taken + (order[i],))
        if inc.weight > cap:
            inc.status = "infeasible"                   # over capacity -> prune
        else:
            if inc.value > best_value:                  # feasible node improves the best answer
                best_value, best_node = inc.value, inc
                best_history.append((inc.id, best_value))
            if inc.level == n:
                inc.status = "leaf"                     # complete assignment, nothing left to branch on
            elif inc.bound > best_value:
                heapq.heappush(heap, (-inc.bound, inc))
            else:
                inc.status = "pruned"
                inc.prune_best = best_value
        # ---- branch 2: EXCLUDE item `level` ----
        exc = new_node(i + 1, node.weight, node.value, node.id, "exclude", node.taken)
        if exc.level == n:
            exc.status = "leaf"                         # complete assignment
        elif exc.bound > best_value:
            heapq.heappush(heap, (-exc.bound, exc))
        else:
            exc.status = "pruned"
            exc.prune_best = best_value

    # nodes left in the heap when it empties were all handled above; mark any 'live' ones
    for nd in nodes:
        if nd.status == "live":
            nd.status = "pruned"
    return nodes, best_value, best_node, best_history


def main():
    nodes, best_value, best_node, best_history = knapsack_bnb()
    n = len(WEIGHTS)
    print("=== 0/1 Knapsack by Branch and Bound ===\n")
    print(f"Weights  : {WEIGHTS}\nValues   : {VALUES}\nCapacity : {CAPACITY}")
    print("Ratios v/w:", [round(v / w, 2) for v, w in zip(VALUES, WEIGHTS)], "(items already sorted)\n")

    print("Node table  (level = items decided; bound = fractional upper bound)")
    print(f"{'ID':>3} {'Parent':>6} {'Branch':>8} {'Lvl':>3} {'Weight':>6} {'Value':>5} {'Bound':>8}  Status")
    for nd in nodes:
        par = "-" if nd.parent is None else nd.parent
        br = nd.decision or "root"
        st = nd.status
        if st == "expanded":
            st = f"expanded (#{nd.order})"
        elif st == "pruned":
            st = f"PRUNED (bound {nd.bound:.2f} <= best {nd.prune_best})"
        elif st == "leaf":
            st = "LEAF (complete solution)" + ("  <== OPTIMAL" if nd is best_node else "")
        elif st == "infeasible":
            st = "PRUNED (weight > capacity)"
        print(f"{nd.id:>3} {par:>6} {br:>8} {nd.level:>3} {nd.weight:>6} {nd.value:>5} {nd.bound:>8.2f}  {st}")

    print("\nBest-value updates:", ", ".join(f"node {i} -> {b}" for i, b in best_history))
    items = sorted(best_node.taken)
    print(f"\nOptimal items  : {[i + 1 for i in items]} (1-indexed)  "
          f"weights {[WEIGHTS[i] for i in items]}  values {[VALUES[i] for i in items]}")
    print(f"Total weight   : {best_node.weight} / {CAPACITY}")
    print(f"Optimal value  : {best_value}")
    pruned = sum(1 for nd in nodes if nd.status in ("pruned", "infeasible"))
    print(f"Nodes generated: {len(nodes)}   pruned: {pruned}   full tree would have {2 ** (n + 1) - 1}")


if __name__ == "__main__":
    main()
