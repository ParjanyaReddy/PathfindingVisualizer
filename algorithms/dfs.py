"""
Depth-First Search (DFS) Algorithm

Time Complexity: O(V + E) where V = vertices (nodes), E = edges
Space Complexity: O(V) for the recursion stack and visited set

DFS explores as far as possible along each branch before backtracking.
It does NOT guarantee the shortest path and is included for comparison
to demonstrate non-optimal pathfinding behavior.

This is a generator function that yields after each step to enable real-time
visualization of the algorithm's progress.
"""

from typing import Generator, Tuple, Optional


def dfs(grid, start, end) -> Generator[Tuple[str, any, int], None, Optional[list]]:
    """
    Depth-First Search algorithm for pathfinding (non-optimal).
    
    DFS uses a LIFO stack (implemented iteratively) to explore paths deeply
    before backtracking. This means it will find A path, but not necessarily
    the shortest path.
    
    Time Complexity: O(V + E)
        - V = number of vertices (grid cells)
        - E = number of edges (connections between cells)
    
    Space Complexity: O(V)
        - Stack can hold all nodes in worst case
        - Visited set tracks all explored nodes
    
    Note: DFS is included to demonstrate non-optimal pathfinding. Compare its
    results with BFS/Dijkstra/A* to see how it may find longer paths.
    
    Args:
        grid: Grid object containing all nodes
        start: Starting Node
        end: Target/End Node
    
    Yields:
        Tuple of (event_type, node/path, visited_count)
        - ('visit', node, count): Node being visited
        - ('path', path_list, count): Final path found
        - ('no_path', None, count): No path exists
    
    Returns:
        List of nodes representing the path, or None if no path exists
    """
    # Initialize the LIFO stack with the start node
    stack = [start]
    
    # Track visited nodes (using set for O(1) lookup)
    visited = {start}
    visited_count = 0
    
    # Update neighbors before starting
    grid.update_all_neighbors()
    
    while stack:
        # Pop the last node (LIFO - this is what makes it DFS)
        current = stack.pop()
        visited_count += 1
        
        # Check if we've reached the goal
        if current == end:
            # Reconstruct and return the path
            path = _reconstruct_path(end)
            yield ('path', path, visited_count)
            return path
        
        # Mark current node as visited (for visualization)
        if current != start:
            current.make_visited(visited_count)
            yield ('visit', current, visited_count)
        
        # Explore all unvisited neighbors
        # Reverse order to maintain consistent direction preference
        for neighbor in reversed(current.neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                stack.append(neighbor)
    
    # No path found
    yield ('no_path', None, visited_count)
    return None


def _reconstruct_path(end_node) -> list:
    """
    Reconstruct the path from end to start by following parent pointers.
    
    Time Complexity: O(P) where P = path length
    
    Args:
        end_node: The destination node
    
    Returns:
        List of nodes from start to end (inclusive)
    """
    path = []
    current = end_node
    
    while current is not None:
        path.append(current)
        current = current.parent
    
    # Reverse to get path from start to end
    path.reverse()
    return path
