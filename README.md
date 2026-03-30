# Convex Layers: Computational Geometry Framework and Comparative Analysis

This repository contains a research-oriented framework for the computation and analysis of **Convex Layers** (Onion Decomposition) in a 2D Euclidean plane. The project implements a suite of classical and optimal algorithms to evaluate their performance across diverse mathematical point distributions, ranging from uniform random sets to complex fractal geometries.

## Overview

The problem of Convex Layers involves the recursive computation of nested convex hulls. Given a set of points $P$, the first layer $L_1$ is the convex hull of $P$. Subsequent layers $L_i$ are defined as the convex hull of $P \setminus \bigcup_{j=1}^{i-1} L_j$.

This framework provides a benchmarking environment to analyze:
* **Asymptotic Efficiency:** Comparing $O(n \log n)$ algorithms against output-sensitive $O(n \log h)$ approaches.
* **Degenerate Case Handling:** Performance under near-collinearity and high-density point duplication.
* **Geometric Distributions:** Behavior of layer growth $k$ in fractals versus random uniform distributions.

## Implemented Algorithms

The suite includes five static algorithms and a specialized dynamic maintenance approach:

| Algorithm | Theoretical Complexity | Implementation Characteristics |
| :--- | :--- | :--- |
| **Chan's Algorithm** | $O(n \log h)$ | Optimal output-sensitive approach combining divide-and-conquer with binary search. |
| **Graham Scan** | $O(n \log n)$ | Standard stack-based approach utilizing polar angle sorting. |
| **Andrew's Monotone Chain** | $O(n \log n)$ | Robust implementation using lexicographical sorting; highly stable. |
| **Quickhull** | $O(n \log n)$ average | Divide-and-conquer strategy; sensitive to $O(n^2)$ worst-case distributions. |
| **Jarvis March** | $O(n \cdot h)$ | Gift-wrapping technique; efficient for minimal hull sizes. |

### Dynamic Maintenance
The framework includes a **Dynamic Peeling Algorithm** for point insertion and deletion. It utilizes a localized recomputation logic to maintain the hierarchical structure without full reconstruction, achieving practical update times between $O(n)$ and $O(nh)$.

## Mathematical Distributions

To evaluate algorithmic robustness, the framework generates datasets based on:
* **Fractal Geometries:** Sierpiński Triangle and Koch Snowflake approximations.
* **Parametric Spirals:** Fibonacci Spirals utilizing the Golden Angle ($\alpha \approx 2.399963$).
* **Edge Cases:** Near-collinear distributions and point sets with high replication (duplicates).

## Benchmarking Suite

The internal benchmarking module facilitates automated testing across variable input sizes ($n=10^2$ to $n=10^5$). It records:
1. **Execution Time:** Total wall-clock time per algorithm/distribution pair.
2. **Memory Complexity:** Peak memory usage during layer decomposition.
3. **Layer Convergence:** Empirical verification of layer growth rates ($k \approx O(\sqrt{n})$ for uniform distributions).

## Technical Requirements

* **Language:** Python 3.9+
* **Dependencies:** NumPy, Matplotlib (for visualization and numerical structures).
* **Environment:** Developed and tested on Intel i7 architectures.

## Documentation

A comprehensive comparative paper detailing the theoretical foundations and empirical results of this study is included in the repository as `Convex_Layers_Paper.pdf`.

 
**Contact:** anca.stanoev04@e-uvt.ro
