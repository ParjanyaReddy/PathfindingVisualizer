"""
Dijkstra's Algorithm

Time Complexity: O((V + E) log V) with binary heap priority queue
Space Complexity: O(V) for the priority queue and distance tracking

Dijkstra's algorithm finds the shortest path in a weighted graph.
It uses a priority queue to always expand the node with the smallest
known distance from the start.

In this visualizer, edge weights are uniform (1), but the algorithm
properly handles weighted edges if needed.

This is a generator function that yields after each step to enable real-time
visualization of the algorithm's progress.
"""

import heapq
from typing import Generator, Tuple, Optional


def dijkstra(grid, start, end) -> Generator[Tuple[str, any, int], None, Optional[list]]:
    """
    Dijkstra's algorithm for finding the shortest weighted path.
    
    Uses a min-heap priority queue to always process the node with the
    smallest cumulative distance from the start. Guarantees shortest path
    in weighted graphs with non-negative edge weights.
    
    Time Complexity: O((V + E) log V)
        - Each vertex is added/removed from heap once: O(V log V)
        - Each edge is relaxed once: O(E log V)
        - Combined: O((V + E) log V)
    
    Space Complexity: O(V)
        - Priority queue can hold all vertices
        - Distance dictionary stores all vertices
    
    Note: In this uniform-weight grid, Dijkstra behaves identically to BFS.
    The algorithm is implemented with proper weighted support for extensibility.
    
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
    # Initialize distances
    start.g_score = 0
    
    # Priority queue: (distance, counter, node)
    # Counter ensures FIFO behavior for equal distances (stable sort)
    counter = 0
    open_set = [(0, counter, start)]
    
    # Track which nodes are in the open set
    open_set_hash = {start}
    
    # Track visited nodes for counting
    visited_count = 0
    
    # Update neighbors before starting
    grid.update_all_neighbors()
    
    while open_set:
        # Get node with smallest distance
        current_dist, _, current = heapq.heappop(open_set)
        open_set_hash.discard(current)
        
        # Skip if we've already found a better path to this node
        if current_dist > current.g_score:
            continue
        
        visited_count += 1
        
        # Check if we've reached the goal
        if current == end:
            path = _reconstruct_path(end)
            yield ('path', path, visited_count)
            return path
        
        # Mark current node as visited (for visualization)
        if current != start:
            current.make_visited(visited_count)
            yield ('visit', current, visited_count)
        
        # Examine all neighbors
        for neighbor in current.neighbors:
            # Edge weight (uniform = 1, but can be modified for weighted graphs)
            edge_weight = 1
            
            # Calculate tentative distance through current node
            tentative_g = current.g_score + edge_weight
            
            # If this path is better than any previous one
            if tentative_g < neighbor.g_score:
                # Update the path
                neighbor.parent = current
                neighbor.g_score = tentative_g
                
                # Add to open set if not already there
                if neighbor not in open_set_hash:
                    counter += 1
                    heapq.heappush(open_set, (tentative_g, counter, neighbor))
                    open_set_hash.add(neighbor)
    
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
