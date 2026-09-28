"""
DAA Macro Project - Unit I : Algorithm Analysis
Project 1 : Sorting Complexity Visualizer

Compares the THEORETICAL (asymptotic) time complexity of
    * Merge Sort           : O(n log n) in every case
    * Quick Sort (average) : O(n log n)
    * Quick Sort (worst)   : O(n^2)
for n = 10, 100 and 1000.

NOTE: The plotted values are the mathematical growth functions n*log2(n)
and n^2 with all constant factors set to 1. They are NOT measured
execution times / benchmarks.

The file also contains working implementations of Merge Sort and Quick Sort,
which are verified for correctness on random inputs of the same sizes.

Usage:
    python Project1_SortingComplexity.py
Output:
    Console table + Visualization.png (needs matplotlib)
"""
import math
import os
import random

SIZES = [10, 100, 1000]


# --------------------------------------------------------------------------
# Merge Sort : divide into halves, sort recursively, merge.  T(n)=2T(n/2)+n
# --------------------------------------------------------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):          # merge step: O(n)
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


# --------------------------------------------------------------------------
# Quick Sort : partition around a pivot, recurse on both sides.
# Average T(n)=2T(n/2)+n  -> O(n log n);  worst T(n)=T(n-1)+n -> O(n^2)
# --------------------------------------------------------------------------
def quick_sort(arr):
    arr = list(arr)

    def partition(lo, hi):                            # Lomuto partition
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    def sort(lo, hi):
        while lo < hi:
            p = partition(lo, hi)
            # recurse on the smaller side first -> recursion depth stays small
            if p - lo < hi - p:
                sort(lo, p - 1); lo = p + 1
            else:
                sort(p + 1, hi); hi = p - 1

    sort(0, len(arr) - 1)
    return arr


# --------------------------------------------------------------------------
# Theoretical growth functions (constants = 1)
# --------------------------------------------------------------------------
def n_log_n(n):
    return n * math.log2(n)


def n_squared(n):
    return n * n


def verify_sorts():
    random.seed(42)
    for n in SIZES:
        data = [random.randint(0, 10_000) for _ in range(n)]
        assert merge_sort(data) == sorted(data), "Merge Sort failed"
        assert quick_sort(data) == sorted(data), "Quick Sort failed"
    print("Correctness check: Merge Sort and Quick Sort sorted all test inputs correctly.\n")


def print_table():
    print("Theoretical growth (constant factors = 1, NOT measured runtimes)")
    print("-" * 78)
    print(f"{'n':>6} | {'Merge Sort':>16} | {'Quick Sort avg':>16} | {'Quick Sort worst':>18}")
    print(f"{'':>6} | {'n log2 n':>16} | {'n log2 n':>16} | {'n^2':>18}")
    print("-" * 78)
    for n in SIZES:
        print(f"{n:>6} | {n_log_n(n):>16,.2f} | {n_log_n(n):>16,.2f} | {n_squared(n):>18,.0f}")
    print("-" * 78)
    print(f"Worst/Average ratio at n=1000 : {n_squared(1000) / n_log_n(1000):.1f}x")


def plot(path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    merge = [n_log_n(n) for n in SIZES]
    q_avg = [n_log_n(n) for n in SIZES]
    q_worst = [n_squared(n) for n in SIZES]

    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=150)
    ax.plot(SIZES, q_worst, "s-", color="#d62728", lw=2.6, ms=9,
            label="Quick Sort worst case  O(n²)")
    ax.plot(SIZES, merge, "o-", color="#1f77b4", lw=2.6, ms=9,
            label="Merge Sort  O(n log n)  (all cases)")
    ax.plot(SIZES, q_avg, "^--", color="#2ca02c", lw=2.2, ms=8,
            label="Quick Sort average case  O(n log n)")

    for n, m, w in zip(SIZES, merge, q_worst):
        ax.annotate(f"{m:,.0f}", (n, m), textcoords="offset points", xytext=(0, -20),
                    ha="center", fontsize=10, color="#1f77b4", fontweight="bold")
        ax.annotate(f"{w:,.0f}", (n, w), textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=10, color="#d62728", fontweight="bold")

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(SIZES); ax.set_xticklabels([f"n = {n}" for n in SIZES], fontsize=11)
    ax.set_xlim(6, 1700); ax.set_ylim(15, 4e6)
    ax.set_xlabel("Input size n", fontsize=12)
    ax.set_ylabel("Growth function value (log scale, constants = 1)", fontsize=12)
    ax.set_title("Merge Sort vs Quick Sort - Theoretical Time Complexity Growth\n"
                 "(asymptotic functions, NOT measured execution times)", fontsize=14, fontweight="bold")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=11, loc="upper left")
    ax.text(0.99, 0.03, "Merge Sort and Quick Sort (average) coincide: both grow as n log₂ n",
            transform=ax.transAxes, ha="right", fontsize=9.5, style="italic", color="#444")
    fig.tight_layout()
    fig.savefig(path)
    print(f"Chart saved to {path}")


if __name__ == "__main__":
    verify_sorts()
    print_table()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Visualization.png")
    try:
        plot(out)
    except ImportError:
        print("matplotlib not installed - skipping chart (pip install matplotlib).")
