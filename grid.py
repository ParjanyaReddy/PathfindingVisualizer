"""
Pathfinding Algorithm Visualizer - Grid Class
Manages the 2D array of nodes and provides grid operations.
"""

from node import Node
from constants import ROWS, COLS, NODE_SIZE, GRID_SIZE


class Grid:
    """
    Manages a 2D array of Node objects for the pathfinding visualizer.
    
    Attributes:
        rows (int): Number of rows in the grid
        cols (int): Number of columns in the grid
        node_size (int): Size of each node in pixels
        nodes (list): 2D list of Node objects
        start_node (Node): Reference to the start node
        end_node (Node): Reference to the end node
    """
    
    def __init__(self, rows: int = ROWS, cols: int = COLS, node_size: int = NODE_SIZE):
        """
        Initialize the grid with specified dimensions.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            node_size: Size of each node in pixels
        """
        self.rows = rows
        self.cols = cols
        self.node_size = node_size
        self.nodes = []
        self.start_node = None
        self.end_node = None
        
        self._create_grid()
    
    def _create_grid(self) -> None:
        """Create the 2D array of Node objects."""
        self.nodes = []
        for row in range(self.rows):
            row_nodes = []
            for col in range(self.cols):
                node = Node(row, col, self.node_size)
                row_nodes.append(node)
            self.nodes.append(row_nodes)
    
    # ========================================================================
    # NODE ACCESS
    # ========================================================================
    
    def get_node(self, row: int, col: int) -> Node:
        """
        Get a node at the specified position.
        
        Args:
            row: Row index
            col: Column index
        
        Returns:
            Node at the specified position, or None if out of bounds
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.nodes[row][col]
        return None
    
    def get_clicked_node(self, pos: tuple) -> Node:
        """
        Get the node at a given pixel position.
        
        Args:
            pos: (x, y) pixel coordinates
        
        Returns:
            Node at the clicked position, or None if out of grid bounds
        """
        x, y = pos
        
        # Check if click is within grid bounds
        if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
            return None
        
        col = x // self.node_size
        row = y // self.node_size
        
        return self.get_node(row, col)
    
    # ========================================================================
    # GRID OPERATIONS
    # ========================================================================
    
    def reset(self) -> None:
        """Reset the entire grid to default state."""
        self.start_node = None
        self.end_node = None
        
        for row in self.nodes:
            for node in row:
                node.reset()
    
    def clear_path(self) -> None:
        """
        Clear only the path visualization (visited nodes, path).
        Keeps start, end, and barrier nodes intact.
        """
        for row in self.nodes:
            for node in row:
                node.clear_path_data()
    
    def update_all_neighbors(self) -> None:
        """Update neighbor lists for all nodes in the grid."""
        for row in self.nodes:
            for node in row:
                node.update_neighbors(self.nodes)
    
    # ========================================================================
    # START/END MANAGEMENT
    # ========================================================================
    
    def set_start(self, node: Node) -> bool:
        """
        Set a node as the start node.
        
        Args:
            node: Node to set as start
        
        Returns:
            True if start was set successfully
        """
        if node is None or node.is_end or node.is_barrier:
            return False
        
        # Clear previous start
        if self.start_node is not None:
            self.start_node.reset()
        
        node.make_start()
        self.start_node = node
        return True
    
    def set_end(self, node: Node) -> bool:
        """
        Set a node as the end node.
        
        Args:
            node: Node to set as end
        
        Returns:
            True if end was set successfully
        """
        if node is None or node.is_start or node.is_barrier:
            return False
        
        # Clear previous end
        if self.end_node is not None:
            self.end_node.reset()
        
        node.make_end()
        self.end_node = node
        return True
    
    def has_start_and_end(self) -> bool:
        """Check if both start and end nodes are set."""
        return self.start_node is not None and self.end_node is not None
    
    # ========================================================================
    # BARRIER MANAGEMENT
    # ========================================================================
    
    def toggle_barrier(self, node: Node) -> None:
        """
        Toggle a node as a barrier.
        
        Args:
            node: Node to toggle
        """
        if node is None or node.is_start or node.is_end:
            return
        
        if node.is_barrier:
            node.reset()
        else:
            node.make_barrier()
    
    def set_barrier(self, node: Node) -> None:
        """
        Set a node as a barrier (for dragging).
        
        Args:
            node: Node to set as barrier
        """
        if node is None or node.is_start or node.is_end or node.is_barrier:
            return
        node.make_barrier()
    
    def clear_node(self, node: Node) -> None:
        """
        Clear a node (reset to default).
        Also clears start/end references if applicable.
        
        Args:
            node: Node to clear
        """
        if node is None:
            return
        
        if node == self.start_node:
            self.start_node = None
        elif node == self.end_node:
            self.end_node = None
        
        node.reset()
    
    # ========================================================================
    # UTILITY METHODS
    # ========================================================================
    
    def get_all_nodes(self) -> list:
        """Return a flat list of all nodes in the grid."""
        return [node for row in self.nodes for node in row]
    
    def get_barrier_count(self) -> int:
        """Return the number of barrier nodes."""
        return sum(1 for node in self.get_all_nodes() if node.is_barrier)
    
    def __iter__(self):
        """Iterate over all rows in the grid."""
        return iter(self.nodes)
    
    def __getitem__(self, index: int) -> list:
        """Access a row by index."""
        return self.nodes[index]
    
    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Grid({self.rows}x{self.cols}, barriers={self.get_barrier_count()})"
