# AI_PATHFINDER_PROJECT
AI Pathfinder Visualizer
A Python-based interactive tool that demonstrates various Artificial Intelligence search algorithms on a 2D grid. The project features a custom GUI built with matplotlib that visualizes the exploration process in real-time, highlighting the frontier, explored nodes, and the final path.

Key Features:

Multiple Search Algorithms: Includes Breadth-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS), Depth-Limited Search (DLS), Iterative Deepening DFS (IDDFS), and Bidirectional Search.

Mandatory Movement Logic: Implements a specific movement priority (Up, Right, Bottom, Bottom-Right, Left, Top-Left).

Real-time Visualization: Uses a soft-themed "Pastel" GUI to track the algorithm's progress step-by-step.

Obstacle Handling: Includes static walls to simulate complex pathfinding environments.
Implementation Architecture:
The system utilizes a modular AIPathfinder class to manage the environment state and search logic. The $10 \times 10$ grid environment is modeled using a NumPy coordinate system, featuring integrated collision detection for static obstacles.
Search Algorithms Included
Uninformed Search: Breadth-First Search (BFS), Depth-First Search (DFS), and Depth-Limited Search (DLS).

Optimal Search: Uniform Cost Search (UCS) utilizing a priority queue (heapq) for cost-efficient pathing.

Iterative & Complex Search: Iterative Deepening DFS (IDDFS) and Bidirectional Search for optimized state-space traversal.
The visualization layer is built on Matplotlib, utilizing a customized "Pastel" design language to differentiate between various search states:

Frontier Nodes: Purple circles representing the set of nodes currently scheduled for expansion.

Explored Set: Pink squares representing states already visited, preventing infinite loops and redundant processing.

Optimal Path: A high-contrast magenta polyline demonstrating the final solution derived by the algorithm.
