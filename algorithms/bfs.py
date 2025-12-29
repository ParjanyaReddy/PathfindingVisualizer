"""
Breadth-First Search (BFS) Algorithm

Time Complexity: O(V + E) where V = vertices (nodes), E = edges
Space Complexity: O(V) for the queue and visited set

BFS explores all neighbors at the current depth before moving to the next level.
It guarantees the shortest path in an unweighted graph.

This is a generator function that yields after each step to enable real-time
visualization of the algorithm's progress.
"""

from collections import deque
from typing import Generator, Tuple, Optional


def bfs(grid, start, end) -> Generator[Tuple[str, any, int], None, Optional[list]]:
    """
    Breadth-First Search algorithm for finding the shortest unweighted path.
    
    BFS uses a FIFO queue to explore nodes level by level, ensuring we find
    the shortest path (in terms of number of edges) from start to end.
    
    Time Complexity: O(V + E)
        - V = number of vertices (grid cells)
        - E = number of edges (connections between cells)
        - In a grid, E ≈ 4V, so effectively O(V)
    
    Space Complexity: O(V)
        - Queue can hold all nodes in worst case
        - Visited set tracks all explored nodes
    
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
    # Initialize the FIFO queue with the start node
    queue = deque([start])
    
    # Track visited nodes (using set for O(1) lookup)
    visited = {start}
    visited_count = 0
    
    # Update neighbors before starting
    grid.update_all_neighbors()
    
    while queue:
        # Dequeue the first node (FIFO)
        current = queue.popleft()
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
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                neighbor.parent = current
                queue.append(neighbor)
    
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
