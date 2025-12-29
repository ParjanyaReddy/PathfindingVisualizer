"""
Pathfinding Algorithm Visualizer - Node Class
Represents a single cell in the grid with state management and neighbor tracking.
"""

from constants import (
    STATE_DEFAULT, STATE_START, STATE_END, STATE_BARRIER, STATE_VISITED, STATE_PATH, STATE_FRONTIER,
    COLOR_DEFAULT, COLOR_START, COLOR_END, COLOR_BARRIER, COLOR_PATH, VISITED_GRADIENT,
    DIRECTIONS, ROWS, COLS
)


class Node:
    """
    Represents a single cell/node in the pathfinding grid.
    
    Attributes:
        row (int): Row position in the grid
        col (int): Column position in the grid
        x (int): Pixel x-coordinate for rendering
        y (int): Pixel y-coordinate for rendering
        size (int): Width/height of the node in pixels
        state (int): Current state of the node (default, start, end, barrier, etc.)
        neighbors (list): List of adjacent valid nodes
        parent (Node): Parent node for path reconstruction
        g_score (float): Cost from start to this node (for Dijkstra/A*)
        f_score (float): Total estimated cost (for A*)
        visited_order (int): Order in which node was visited (for gradient coloring)
    """
    
    def __init__(self, row: int, col: int, size: int):
        """
        Initialize a node with position and size.
        
        Args:
            row: Row position in the grid
            col: Column position in the grid
            size: Width/height of the node in pixels
        """
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.size = size
        
        # State management
        self.state = STATE_DEFAULT
        self.neighbors = []
        self.parent = None
        
        # Algorithm-specific scores
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.visited_order = 0
    
    # ========================================================================
    # STATE QUERIES
    # ========================================================================
    
    @property
    def is_start(self) -> bool:
        """Check if this node is the start node."""
        return self.state == STATE_START
    
    @property
    def is_end(self) -> bool:
        """Check if this node is the end node."""
        return self.state == STATE_END
    
    @property
    def is_barrier(self) -> bool:
        """Check if this node is a barrier/wall."""
        return self.state == STATE_BARRIER
    
    @property
    def is_visited(self) -> bool:
        """Check if this node has been visited."""
        return self.state == STATE_VISITED
    
    @property
    def is_path(self) -> bool:
        """Check if this node is part of the final path."""
        return self.state == STATE_PATH
    
    @property
    def is_frontier(self) -> bool:
        """Check if this node is in the frontier/queue."""
        return self.state == STATE_FRONTIER
    
    @property
    def is_empty(self) -> bool:
        """Check if this node is in default state (can be modified)."""
        return self.state == STATE_DEFAULT
    
    # ========================================================================
    # STATE MODIFIERS
    # ========================================================================
    
    def reset(self) -> None:
        """Reset node to default state and clear algorithm data."""
        self.state = STATE_DEFAULT
        self.parent = None
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.visited_order = 0
    
    def make_start(self) -> None:
        """Set this node as the start node."""
        self.state = STATE_START
    
    def make_end(self) -> None:
        """Set this node as the end node."""
        self.state = STATE_END
    
    def make_barrier(self) -> None:
        """Set this node as a barrier/wall."""
        self.state = STATE_BARRIER
    
    def make_visited(self, order: int = 0) -> None:
        """
        Mark this node as visited.
        
        Args:
            order: The order in which this node was visited (for gradient coloring)
        """
        self.state = STATE_VISITED
        self.visited_order = order
    
    def make_path(self) -> None:
        """Mark this node as part of the final path."""
        self.state = STATE_PATH
    
    def make_frontier(self) -> None:
        """Mark this node as being in the frontier/queue."""
        self.state = STATE_FRONTIER
    
    def clear_path_data(self) -> None:
        """
        Clear path-related data without changing wall status.
        Used when clearing path but keeping walls.
        """
        if self.state in (STATE_VISITED, STATE_PATH, STATE_FRONTIER):
            self.state = STATE_DEFAULT
        self.parent = None
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.visited_order = 0
    
    # ========================================================================
    # COLOR CALCULATION
    # ========================================================================
    
    def get_color(self, max_visited_order: int = 1) -> tuple:
        """
        Get the current color of the node based on its state.
        
        For visited nodes, returns a gradient color based on visit order.
        
        Args:
            max_visited_order: Maximum visited order in the algorithm run
                              (used to calculate gradient position)
        
        Returns:
            RGB tuple representing the node's color
        """
        if self.state == STATE_DEFAULT:
            return COLOR_DEFAULT
        elif self.state == STATE_START:
            return COLOR_START
        elif self.state == STATE_END:
            return COLOR_END
        elif self.state == STATE_BARRIER:
            return COLOR_BARRIER
        elif self.state == STATE_PATH:
            return COLOR_PATH
        elif self.state == STATE_VISITED:
            # Calculate gradient color based on visit order
            return self._get_gradient_color(max_visited_order)
        elif self.state == STATE_FRONTIER:
            # Frontier nodes get a slightly different shade
            return (100, 200, 220)  # Light cyan for frontier
        return COLOR_DEFAULT
    
    def _get_gradient_color(self, max_order: int) -> tuple:
        """
        Calculate gradient color for visited nodes.
        
        Interpolates between colors in VISITED_GRADIENT based on visit order.
        
        Args:
            max_order: Maximum visit order for normalization
        
        Returns:
            RGB tuple for the gradient color
        """
        if max_order <= 1:
            return VISITED_GRADIENT[0]
        
        # Normalize visit order to [0, 1]
        t = self.visited_order / max_order
        
        # Map to gradient index
        num_colors = len(VISITED_GRADIENT)
        scaled = t * (num_colors - 1)
        idx = int(scaled)
        frac = scaled - idx
        
        # Clamp index
        if idx >= num_colors - 1:
            return VISITED_GRADIENT[-1]
        
        # Interpolate between two adjacent colors
        c1 = VISITED_GRADIENT[idx]
        c2 = VISITED_GRADIENT[idx + 1]
        
        return (
            int(c1[0] + (c2[0] - c1[0]) * frac),
            int(c1[1] + (c2[1] - c1[1]) * frac),
            int(c1[2] + (c2[2] - c1[2]) * frac),
        )
    
    # ========================================================================
    # NEIGHBOR MANAGEMENT
    # ========================================================================
    
    def update_neighbors(self, grid: list) -> None:
        """
        Update the list of valid neighbors for this node.
        
        Neighbors are adjacent nodes that are not barriers.
        Uses 4-directional movement (up, down, left, right).
        
        Args:
            grid: 2D list of Node objects
        """
        self.neighbors = []
        
        for dr, dc in DIRECTIONS:
            new_row = self.row + dr
            new_col = self.col + dc
            
            # Check bounds
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                neighbor = grid[new_row][new_col]
                # Only add non-barrier neighbors
                if not neighbor.is_barrier:
                    self.neighbors.append(neighbor)
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_position(self) -> tuple:
        """Return the (row, col) position of this node."""
        return (self.row, self.col)
    
    def __lt__(self, other: 'Node') -> bool:
        """
        Less-than comparison for priority queue ordering.
        Nodes are compared by f_score, then g_score.
        """
        if self.f_score == other.f_score:
            return self.g_score < other.g_score
        return self.f_score < other.f_score
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Node({self.row}, {self.col}, state={self.state})"
