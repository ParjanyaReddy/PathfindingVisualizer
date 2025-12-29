"""
Pathfinding Algorithm Visualizer - Renderer
Handles all PyGame rendering including grid, nodes, sidebar, and UI elements.
"""

import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, SIDEBAR_WIDTH,
    BACKGROUND, SIDEBAR_BG, GRID_LINE,
    TEXT_COLOR, TEXT_ACCENT, TEXT_HIGHLIGHT,
    FONT_SIZE_LARGE, FONT_SIZE_MEDIUM, FONT_SIZE_SMALL,
    ALGORITHMS, NODE_SIZE
)


class Renderer:
    """
    Handles all PyGame rendering for the pathfinding visualizer.
    
    Attributes:
        screen: PyGame display surface
        fonts: Dictionary of PyGame font objects
        max_visited_order: Maximum visited order for gradient calculation
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the renderer with a PyGame screen.
        
        Args:
            screen: PyGame display surface
        """
        self.screen = screen
        self.max_visited_order = 1
        
        # Initialize fonts
        pygame.font.init()
        self.fonts = {
            'large': pygame.font.SysFont('Segoe UI', FONT_SIZE_LARGE, bold=True),
            'medium': pygame.font.SysFont('Segoe UI', FONT_SIZE_MEDIUM),
            'small': pygame.font.SysFont('Segoe UI', FONT_SIZE_SMALL),
        }
    
    def draw_frame(self, grid, stats: dict, current_algorithm: int) -> None:
        """
        Draw a complete frame including grid and sidebar.
        
        Args:
            grid: Grid object to render
            stats: Dictionary containing performance metrics
            current_algorithm: Currently selected algorithm index
        """
        # Clear screen
        self.screen.fill(BACKGROUND)
        
        # Draw grid area
        self._draw_grid(grid)
        
        # Draw sidebar
        self._draw_sidebar(stats, current_algorithm)
        
        # Update display
        pygame.display.flip()
    
    def _draw_grid(self, grid) -> None:
        """
        Draw the entire grid including all nodes and grid lines.
        
        Args:
            grid: Grid object to render
        """
        # Draw all nodes
        for row in grid.nodes:
            for node in row:
                self._draw_node(node)
        
        # Draw grid lines
        for i in range(grid.rows + 1):
            # Horizontal lines
            pygame.draw.line(
                self.screen,
                GRID_LINE,
                (0, i * NODE_SIZE),
                (GRID_SIZE, i * NODE_SIZE),
                1
            )
        
        for j in range(grid.cols + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                GRID_LINE,
                (j * NODE_SIZE, 0),
                (j * NODE_SIZE, GRID_SIZE),
                1
            )
    
    def _draw_node(self, node) -> None:
        """
        Draw a single node with its current color.
        
        Args:
            node: Node object to draw
        """
        color = node.get_color(self.max_visited_order)
        
        pygame.draw.rect(
            self.screen,
            color,
            (node.x, node.y, node.size, node.size)
        )
    
    def _draw_sidebar(self, stats: dict, current_algorithm: int) -> None:
        """
        Draw the sidebar with stats and controls.
        
        Args:
            stats: Dictionary containing performance metrics
            current_algorithm: Currently selected algorithm index
        """
        # Draw sidebar background
        sidebar_rect = pygame.Rect(GRID_SIZE, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, SIDEBAR_BG, sidebar_rect)
        
        # Draw separator line
        pygame.draw.line(
            self.screen,
            GRID_LINE,
            (GRID_SIZE, 0),
            (GRID_SIZE, WINDOW_HEIGHT),
            2
        )
        
        x = GRID_SIZE + 15
        y = 20
        line_height = 30
        
        # Title
        title = self.fonts['large'].render("PATHFINDER", True, TEXT_ACCENT)
        self.screen.blit(title, (x, y))
        y += line_height + 20
        
        # Current Algorithm
        algo_label = self.fonts['small'].render("Algorithm:", True, TEXT_COLOR)
        self.screen.blit(algo_label, (x, y))
        y += line_height - 5
        
        algo_name = ALGORITHMS.get(current_algorithm, "None")
        algo_text = self.fonts['medium'].render(algo_name, True, TEXT_HIGHLIGHT)
        self.screen.blit(algo_text, (x, y))
        y += line_height + 15
        
        # Separator
        pygame.draw.line(self.screen, GRID_LINE, (x, y), (GRID_SIZE + SIDEBAR_WIDTH - 15, y), 1)
        y += 15
        
        # Stats Section
        stats_title = self.fonts['medium'].render("Statistics", True, TEXT_ACCENT)
        self.screen.blit(stats_title, (x, y))
        y += line_height + 5
        
        # Time elapsed
        time_text = f"Time: {stats.get('time', 0):.2f} ms"
        time_surface = self.fonts['small'].render(time_text, True, TEXT_COLOR)
        self.screen.blit(time_surface, (x, y))
        y += line_height - 5
        
        # Nodes visited
        visited_text = f"Nodes Visited: {stats.get('visited', 0)}"
        visited_surface = self.fonts['small'].render(visited_text, True, TEXT_COLOR)
        self.screen.blit(visited_surface, (x, y))
        y += line_height - 5
        
        # Path length
        path_text = f"Path Length: {stats.get('path_length', 0)}"
        path_surface = self.fonts['small'].render(path_text, True, TEXT_COLOR)
        self.screen.blit(path_surface, (x, y))
        y += line_height + 15
        
        # Separator
        pygame.draw.line(self.screen, GRID_LINE, (x, y), (GRID_SIZE + SIDEBAR_WIDTH - 15, y), 1)
        y += 15
        
        # Status
        status_title = self.fonts['medium'].render("Status", True, TEXT_ACCENT)
        self.screen.blit(status_title, (x, y))
        y += line_height
        
        status = stats.get('status', 'Ready')
        status_color = TEXT_HIGHLIGHT if status == 'Path Found!' else TEXT_COLOR
        status_surface = self.fonts['small'].render(status, True, status_color)
        self.screen.blit(status_surface, (x, y))
        y += line_height + 15
        
        # Separator
        pygame.draw.line(self.screen, GRID_LINE, (x, y), (GRID_SIZE + SIDEBAR_WIDTH - 15, y), 1)
        y += 15
        
        # Speed indicator
        speed_title = self.fonts['medium'].render("Animation Speed", True, TEXT_ACCENT)
        self.screen.blit(speed_title, (x, y))
        y += line_height
        
        delay = stats.get('delay', 10)
        speed_desc = "Fast" if delay < 15 else "Medium" if delay < 50 else "Slow"
        speed_text = f"{speed_desc} ({delay}ms)"
        speed_surface = self.fonts['small'].render(speed_text, True, TEXT_COLOR)
        self.screen.blit(speed_surface, (x, y))
        y += line_height + 20
        
        # Separator
        pygame.draw.line(self.screen, GRID_LINE, (x, y), (GRID_SIZE + SIDEBAR_WIDTH - 15, y), 1)
        y += 15
        
        # Controls Section
        controls_title = self.fonts['medium'].render("Controls", True, TEXT_ACCENT)
        self.screen.blit(controls_title, (x, y))
        y += line_height + 5
        
        controls = [
            "Left Click: Place nodes",
            "Right Click: Erase",
            "SPACE: Start search",
            "C: Clear board",
            "R: Random maze",
            "1-4: Select algorithm",
            "+/-: Adjust speed",
        ]
        
        for control in controls:
            control_surface = self.fonts['small'].render(control, True, TEXT_COLOR)
            self.screen.blit(control_surface, (x, y))
            y += line_height - 7
    
    def update_max_visited(self, order: int) -> None:
        """
        Update the maximum visited order for gradient calculation.
        
        Args:
            order: Current maximum visited order
        """
        if order > self.max_visited_order:
            self.max_visited_order = order
    
    def reset_visited_order(self) -> None:
        """Reset the maximum visited order."""
        self.max_visited_order = 1
    
    def update_caption(self, text: str) -> None:
        """
        Update the window caption.
        
        Args:
            text: Text to display in window title
        """
        pygame.display.set_caption(text)
