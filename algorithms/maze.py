"""
Recursive Backtracker Maze Generation Algorithm

Time Complexity: O(V) where V = number of cells
Space Complexity: O(V) for the recursion stack

The Recursive Backtracker (also known as Randomized DFS) creates perfect mazes
by carving passages through an initially filled grid. It guarantees:
- Every cell is reachable from every other cell
- There is exactly one path between any two cells (no loops)

Algorithm:
1. Start with a grid full of walls
2. Choose a starting cell and mark it as passage
3. While there are unvisited cells:
   a. If current cell has unvisited neighbors:
      - Choose a random unvisited neighbor
      - Remove wall between current and neighbor
      - Move to neighbor and mark as visited
   b. Else backtrack to previous cell

This is a generator function that yields after each step to enable real-time
visualization of the maze generation process.
"""

import random
from typing import Generator, Tuple


def recursive_backtracker(grid) -> Generator[Tuple[str, any], None, None]:
    """
    Generate a maze using the Recursive Backtracker algorithm.
    
    Creates a perfect maze (no loops, all cells connected) by performing
    a randomized depth-first search through the grid, carving passages
    as it goes.
    
    Time Complexity: O(V)
        - Each cell is visited exactly once
        - V = rows × cols cells in the grid
    
    Space Complexity: O(V)
        - Stack can grow to contain all cells in worst case
        - Typical case is O(longest path length)
    
    Args:
        grid: Grid object to generate maze in
    
    Yields:
        Tuple of (event_type, node)
        - ('wall', node): Node made into wall
        - ('passage', node): Node carved as passage
        - ('done', None): Maze generation complete
    """
    rows = grid.rows
    cols = grid.cols
    
    # First, fill the entire grid with walls
    for row in grid.nodes:
        for node in row:
            node.make_barrier()
            yield ('wall', node)
    
    # Direction vectors for maze carving (step by 2 to leave walls between passages)
    # Format: (row_step, col_step)
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    # Start from cell (1, 1) to ensure we have a border
    start_row, start_col = 1, 1
    
    # Make sure starting position is valid
    if start_row >= rows or start_col >= cols:
        yield ('done', None)
        return
    
    # Initialize starting cell
    start_cell = grid.nodes[start_row][start_col]
    start_cell.reset()  # Make it a passage
    yield ('passage', start_cell)
    
    # Stack for backtracking: stores (row, col) positions
    stack = [(start_row, start_col)]
    
    # Track visited cells for maze generation
    visited = set()
    visited.add((start_row, start_col))
    
    while stack:
        current_row, current_col = stack[-1]
        
        # Find all unvisited neighbors (2 cells away)
        unvisited_neighbors = []
        
        for dr, dc in directions:
            new_row = current_row + dr
            new_col = current_col + dc
            
            # Check bounds (leaving 1-cell border)
            if 1 <= new_row < rows - 1 and 1 <= new_col < cols - 1:
                if (new_row, new_col) not in visited:
                    unvisited_neighbors.append((new_row, new_col, dr // 2, dc // 2))
        
        if unvisited_neighbors:
            # Choose a random unvisited neighbor
            next_row, next_col, wall_dr, wall_dc = random.choice(unvisited_neighbors)
            
            # Remove wall between current and next cell
            wall_row = current_row + wall_dr
            wall_col = current_col + wall_dc
            
            wall_node = grid.nodes[wall_row][wall_col]
            wall_node.reset()  # Carve passage through wall
            yield ('passage', wall_node)
            
            # Mark neighbor as visited and carve passage
            visited.add((next_row, next_col))
            next_node = grid.nodes[next_row][next_col]
            next_node.reset()  # Carve passage
            yield ('passage', next_node)
            
            # Push neighbor onto stack
            stack.append((next_row, next_col))
        else:
            # No unvisited neighbors, backtrack
            stack.pop()
    
    yield ('done', None)


def generate_maze_instant(grid) -> None:
    """
    Generate a maze instantly without animation.
    
    Useful for quick maze generation when animation is not needed.
    
    Args:
        grid: Grid object to generate maze in
    """
    # Consume all generator events without yielding
    for _ in recursive_backtracker(grid):
        pass
