"""
A* (A-Star) Search Algorithm

Time Complexity: O((V + E) log V) with binary heap priority queue
Space Complexity: O(V) for the priority queue and score tracking

A* is an informed search algorithm that uses a heuristic to guide its search
toward the goal. It combines the actual cost from start (g) with an estimated
cost to goal (h) to prioritize exploration.

Heuristic used: Manhattan Distance (optimal for 4-directional grid movement)
    h(n) = |x1 - x2| + |y1 - y2|

The A* algorithm is optimal and complete when using an admissible heuristic
(one that never overestimates the true cost).

This is a generator function that yields after each step to enable real-time
visualization of the algorithm's progress.
"""

import heapq
from typing import Generator, Tuple, Optional


def manhattan_distance(node1, node2) -> int:
    """
    Calculate the Manhattan distance between two nodes.
    
    Manhattan distance is the sum of absolute differences in x and y coordinates.
    It's an admissible heuristic for 4-directional grid movement (never overestimates).
    
    Time Complexity: O(1)
    
    Args:
        node1: First node
        node2: Second node
    
    Returns:
        Manhattan distance between the nodes
    """
    return abs(node1.row - node2.row) + abs(node1.col - node2.col)


def astar(grid, start, end) -> Generator[Tuple[str, any, int], None, Optional[list]]:
    """
    A* Search algorithm for finding the optimal path with heuristic guidance.
    
    A* uses f(n) = g(n) + h(n) where:
        - g(n) = actual cost from start to node n
        - h(n) = estimated cost from node n to goal (heuristic)
        - f(n) = total estimated cost through node n
    
    Time Complexity: O((V + E) log V)
        - Depends heavily on heuristic quality
        - With perfect heuristic: O(d) where d = solution depth
        - With no heuristic (h=0): degrades to Dijkstra O((V+E) log V)
    
    Space Complexity: O(V)
        - Open set (priority queue) can hold all vertices
        - Closed set tracks all visited vertices
    
    The Manhattan distance heuristic is:
        - Admissible: Never overestimates (guarantees optimal path)
        - Consistent: h(n) ≤ cost(n,n') + h(n') for all successors n'
    
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
    # Initialize scores for start node
    start.g_score = 0  # Cost from start
    start.f_score = manhattan_distance(start, end)  # Estimated total cost
    
    # Priority queue: (f_score, counter, node)
    # Counter ensures FIFO for equal f-scores (tie-breaking)
    counter = 0
    open_set = [(start.f_score, counter, start)]
    
    # Track which nodes are in the open set for O(1) lookup
    open_set_hash = {start}
    
    # Track visited nodes for counting
    visited_count = 0
    
    # Update neighbors before starting
    grid.update_all_neighbors()
    
    while open_set:
        # Get node with smallest f_score
        current_f, _, current = heapq.heappop(open_set)
        open_set_hash.discard(current)
        
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
            # Edge weight (uniform = 1)
            edge_weight = 1
            
            # Calculate tentative g_score through current node
            tentative_g = current.g_score + edge_weight
            
            # If this path is better than any previous one
            if tentative_g < neighbor.g_score:
                # Update path and scores
                neighbor.parent = current
                neighbor.g_score = tentative_g
                neighbor.f_score = tentative_g + manhattan_distance(neighbor, end)
                
                # Add to open set if not already there
                if neighbor not in open_set_hash:
                    counter += 1
                    heapq.heappush(open_set, (neighbor.f_score, counter, neighbor))
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
