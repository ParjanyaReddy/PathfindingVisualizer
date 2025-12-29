"""
Pathfinding Algorithms Package
Contains implementations of BFS, DFS, Dijkstra, A*, and maze generation.
"""

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.dijkstra import dijkstra
from algorithms.astar import astar
from algorithms.maze import recursive_backtracker

__all__ = ['bfs', 'dfs', 'dijkstra', 'astar', 'recursive_backtracker']
