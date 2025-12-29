"""
Pathfinding Algorithm Visualizer - Main Application

A professional-grade pathfinding visualizer built with Python and PyGame.
Features BFS, DFS, Dijkstra, A* algorithms and maze generation.

Author: Portfolio Project
Version: 1.0.0

Controls:
    Left Click (1st): Place Start node
    Left Click (2nd): Place End node
    Left Click (drag): Draw walls
    Right Click: Erase node
    SPACE: Start pathfinding
    C: Clear board
    R: Generate random maze
    1-4: Select algorithm (BFS, DFS, Dijkstra, A*)
    +/-: Adjust animation speed
    ESC: Quit
"""

import pygame
import time
import sys

# Add current directory to path for imports
sys.path.insert(0, '.')

from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE,
    ROWS, COLS, NODE_SIZE,
    DEFAULT_ANIMATION_DELAY, MIN_ANIMATION_DELAY, MAX_ANIMATION_DELAY, ANIMATION_STEP,
    ALGORITHMS, BACKGROUND
)
from grid import Grid
from renderer import Renderer
from algorithms import bfs, dfs, dijkstra, astar, recursive_backtracker


class PathfindingVisualizer:
    """
    Main application class for the Pathfinding Algorithm Visualizer.
    
    Manages the game loop, user input, and coordinates between
    the grid, algorithms, and renderer.
    """
    
    def __init__(self):
        """Initialize the visualizer application."""
        # Initialize PyGame
        pygame.init()
        
        # Create window
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pathfinding Visualizer")
        
        # Initialize clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Create grid and renderer
        self.grid = Grid(ROWS, COLS, NODE_SIZE)
        self.renderer = Renderer(self.screen)
        
        # Application state
        self.running = True
        self.is_running_algorithm = False
        self.is_generating_maze = False
        
        # Current algorithm selection (1: BFS, 2: DFS, 3: Dijkstra, 4: A*)
        self.current_algorithm = 4  # Default to A*
        
        # Animation speed (delay in milliseconds)
        self.animation_delay = DEFAULT_ANIMATION_DELAY
        
        # Performance stats
        self.stats = {
            'time': 0,
            'visited': 0,
            'path_length': 0,
            'status': 'Ready',
            'delay': self.animation_delay
        }
        
        # Node placement state
        self.start_placed = False
        self.end_placed = False
    
    def run(self) -> None:
        """Main application loop."""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
    
    def _handle_events(self) -> None:
        """Process all PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.is_running_algorithm and not self.is_generating_maze:
                    self._handle_mouse_click(event.button, event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                if not self.is_running_algorithm and not self.is_generating_maze:
                    self._handle_mouse_drag(event.pos, event.buttons)
    
    def _handle_keydown(self, key: int) -> None:
        """
        Handle keyboard input.
        
        Args:
            key: PyGame key code
        """
        # Don't allow most inputs while algorithm is running
        if self.is_running_algorithm or self.is_generating_maze:
            if key == pygame.K_ESCAPE:
                self.is_running_algorithm = False
                self.is_generating_maze = False
            return
        
        if key == pygame.K_SPACE:
            # Start pathfinding
            self._start_pathfinding()
        
        elif key == pygame.K_c:
            # Clear the board
            self._clear_board()
        
        elif key == pygame.K_r:
            # Generate random maze
            self._generate_maze()
        
        elif key == pygame.K_1:
            self.current_algorithm = 1
            self.stats['status'] = 'Selected: BFS'
        
        elif key == pygame.K_2:
            self.current_algorithm = 2
            self.stats['status'] = 'Selected: DFS'
        
        elif key == pygame.K_3:
            self.current_algorithm = 3
            self.stats['status'] = 'Selected: Dijkstra'
        
        elif key == pygame.K_4:
            self.current_algorithm = 4
            self.stats['status'] = 'Selected: A*'
        
        elif key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
            # Decrease delay (faster animation)
            self.animation_delay = max(MIN_ANIMATION_DELAY, self.animation_delay - ANIMATION_STEP)
            self.stats['delay'] = self.animation_delay
        
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            # Increase delay (slower animation)
            self.animation_delay = min(MAX_ANIMATION_DELAY, self.animation_delay + ANIMATION_STEP)
            self.stats['delay'] = self.animation_delay
        
        elif key == pygame.K_ESCAPE:
            self.running = False
    
    def _handle_mouse_click(self, button: int, pos: tuple) -> None:
        """
        Handle mouse click events.
        
        Args:
            button: Mouse button (1=left, 3=right)
            pos: (x, y) position of click
        """
        node = self.grid.get_clicked_node(pos)
        if node is None:
            return
        
        if button == 1:  # Left click
            if not self.start_placed:
                # Place start node
                if self.grid.set_start(node):
                    self.start_placed = True
                    self.stats['status'] = 'Place end node'
            elif not self.end_placed:
                # Place end node
                if self.grid.set_end(node):
                    self.end_placed = True
                    self.stats['status'] = 'Draw walls or press SPACE'
            else:
                # Place barrier
                self.grid.set_barrier(node)
        
        elif button == 3:  # Right click
            # Clear the node
            if node == self.grid.start_node:
                self.start_placed = False
            elif node == self.grid.end_node:
                self.end_placed = False
            self.grid.clear_node(node)
    
    def _handle_mouse_drag(self, pos: tuple, buttons: tuple) -> None:
        """
        Handle mouse drag events for drawing walls.
        
        Args:
            pos: Current mouse position
            buttons: Tuple of button states (left, middle, right)
        """
        node = self.grid.get_clicked_node(pos)
        if node is None:
            return
        
        if buttons[0]:  # Left button held
            if self.start_placed and self.end_placed:
                self.grid.set_barrier(node)
        
        elif buttons[2]:  # Right button held
            if node == self.grid.start_node:
                self.start_placed = False
            elif node == self.grid.end_node:
                self.end_placed = False
            self.grid.clear_node(node)
    
    def _start_pathfinding(self) -> None:
        """Start the pathfinding algorithm."""
        if not self.grid.has_start_and_end():
            self.stats['status'] = 'Place start & end first!'
            return
        
        # Clear previous path
        self.grid.clear_path()
        self.renderer.reset_visited_order()
        
        # Reset stats
        self.stats['visited'] = 0
        self.stats['path_length'] = 0
        self.stats['status'] = 'Searching...'
        
        # Select algorithm
        algorithms = {
            1: bfs,
            2: dfs,
            3: dijkstra,
            4: astar
        }
        
        algorithm = algorithms.get(self.current_algorithm, astar)
        
        # Run algorithm with animation
        self.is_running_algorithm = True
        start_time = time.time()
        
        # Create generator
        gen = algorithm(self.grid, self.grid.start_node, self.grid.end_node)
        
        # Animate the algorithm
        for event_type, data, visited_count in gen:
            # Check if cancelled
            if not self.is_running_algorithm:
                self.stats['status'] = 'Cancelled'
                return
            
            # Handle events to allow cancellation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.is_running_algorithm = False
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_running_algorithm = False
                    self.stats['status'] = 'Cancelled'
                    return
            
            self.stats['visited'] = visited_count
            self.renderer.update_max_visited(visited_count)
            
            if event_type == 'visit':
                # Update display
                self._render()
                pygame.time.delay(self.animation_delay)
            
            elif event_type == 'path':
                # Path found - animate it
                elapsed_time = (time.time() - start_time) * 1000
                self.stats['time'] = elapsed_time
                self.stats['path_length'] = len(data)
                self.stats['status'] = 'Path Found!'
                
                # Animate the path
                self._animate_path(data)
            
            elif event_type == 'no_path':
                elapsed_time = (time.time() - start_time) * 1000
                self.stats['time'] = elapsed_time
                self.stats['status'] = 'No Path Found!'
        
        self.is_running_algorithm = False
    
    def _animate_path(self, path: list) -> None:
        """
        Animate the final path.
        
        Args:
            path: List of nodes in the path
        """
        for node in path:
            if node != self.grid.start_node and node != self.grid.end_node:
                node.make_path()
                self._render()
                pygame.time.delay(max(self.animation_delay * 2, 20))
    
    def _clear_board(self) -> None:
        """Clear the entire board."""
        self.grid.reset()
        self.start_placed = False
        self.end_placed = False
        self.renderer.reset_visited_order()
        self.stats = {
            'time': 0,
            'visited': 0,
            'path_length': 0,
            'status': 'Board cleared',
            'delay': self.animation_delay
        }
    
    def _generate_maze(self) -> None:
        """Generate a random maze using recursive backtracker."""
        self.is_generating_maze = True
        self.stats['status'] = 'Generating maze...'
        
        # Clear the board first
        self.grid.reset()
        self.start_placed = False
        self.end_placed = False
        self.renderer.reset_visited_order()
        
        # Generate maze
        gen = recursive_backtracker(self.grid)
        
        step_count = 0
        for event_type, node in gen:
            # Check for cancellation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.is_generating_maze = False
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_generating_maze = False
                    self.stats['status'] = 'Maze generation cancelled'
                    return
            
            step_count += 1
            
            # Render every few steps for smooth animation
            if step_count % 3 == 0:
                self._render()
                pygame.time.delay(1)  # Very fast animation for maze
            
            if event_type == 'done':
                break
        
        # Place start and end in corners
        self._place_start_end_in_maze()
        
        self.is_generating_maze = False
        self.stats['status'] = 'Maze generated! Press SPACE'
    
    def _place_start_end_in_maze(self) -> None:
        """Place start and end nodes in the generated maze."""
        # Find valid positions near corners
        # Start: top-left area
        for row in range(1, ROWS - 1):
            for col in range(1, COLS - 1):
                node = self.grid.get_node(row, col)
                if not node.is_barrier:
                    self.grid.set_start(node)
                    self.start_placed = True
                    break
            if self.start_placed:
                break
        
        # End: bottom-right area
        for row in range(ROWS - 2, 0, -1):
            for col in range(COLS - 2, 0, -1):
                node = self.grid.get_node(row, col)
                if not node.is_barrier and not node.is_start:
                    self.grid.set_end(node)
                    self.end_placed = True
                    break
            if self.end_placed:
                break
    
    def _update(self) -> None:
        """Update application state (currently handled in event loop)."""
        pass
    
    def _render(self) -> None:
        """Render the current frame."""
        self.renderer.draw_frame(self.grid, self.stats, self.current_algorithm)


def main():
    """Entry point for the application."""
    app = PathfindingVisualizer()
    app.run()


if __name__ == "__main__":
    main()
