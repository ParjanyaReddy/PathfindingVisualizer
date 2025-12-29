"""
Pathfinding Algorithm Visualizer - Constants & Configuration
Contains color palette (Nord/Dracula theme), grid settings, and UI configuration.
"""

# ============================================================================
# WINDOW CONFIGURATION
# ============================================================================
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
GRID_SIZE = 750  # Square grid area
SIDEBAR_WIDTH = WINDOW_WIDTH - GRID_SIZE  # 250px for stats

# ============================================================================
# GRID CONFIGURATION
# ============================================================================
ROWS = 50
COLS = 50
NODE_SIZE = GRID_SIZE // ROWS  # 15px per node

# ============================================================================
# ANIMATION CONFIGURATION
# ============================================================================
DEFAULT_ANIMATION_DELAY = 10  # milliseconds
MIN_ANIMATION_DELAY = 1
MAX_ANIMATION_DELAY = 100
ANIMATION_STEP = 5

# ============================================================================
# COLOR PALETTE - Nord/Dracula Theme
# ============================================================================

# Background Colors
BACKGROUND = (40, 42, 54)        # Dracula background
SIDEBAR_BG = (30, 32, 44)        # Darker sidebar
GRID_LINE = (68, 71, 90)         # Grid lines

# Node State Colors
COLOR_DEFAULT = (248, 248, 242)  # Off-white
COLOR_START = (80, 250, 123)     # Green (Dracula green)
COLOR_END = (255, 121, 63)       # Orange-red
COLOR_BARRIER = (68, 71, 90)     # Dark grey
COLOR_PATH = (241, 250, 140)     # Yellow (Dracula yellow)

# Visited Node Gradient (Cyan → Purple → Pink)
VISITED_GRADIENT = [
    (139, 233, 253),  # Cyan
    (153, 207, 255),  # Light blue
    (169, 180, 255),  # Periwinkle
    (189, 147, 249),  # Purple (Dracula purple)
    (210, 130, 230),  # Light purple
    (255, 121, 198),  # Pink (Dracula pink)
]

# UI Text Colors
TEXT_COLOR = (248, 248, 242)     # White text
TEXT_ACCENT = (139, 233, 253)    # Cyan accent
TEXT_HIGHLIGHT = (80, 250, 123)  # Green highlight

# ============================================================================
# NODE STATES (for easier state management)
# ============================================================================
STATE_DEFAULT = 0
STATE_START = 1
STATE_END = 2
STATE_BARRIER = 3
STATE_VISITED = 4
STATE_PATH = 5
STATE_FRONTIER = 6  # Nodes in the queue/frontier

# Color mapping for states
STATE_COLORS = {
    STATE_DEFAULT: COLOR_DEFAULT,
    STATE_START: COLOR_START,
    STATE_END: COLOR_END,
    STATE_BARRIER: COLOR_BARRIER,
    STATE_PATH: COLOR_PATH,
}

# ============================================================================
# ALGORITHM NAMES
# ============================================================================
ALGORITHMS = {
    1: "BFS (Breadth-First Search)",
    2: "DFS (Depth-First Search)",
    3: "Dijkstra's Algorithm",
    4: "A* Search",
}

# ============================================================================
# FONT CONFIGURATION
# ============================================================================
FONT_SIZE_LARGE = 28
FONT_SIZE_MEDIUM = 20
FONT_SIZE_SMALL = 16

# ============================================================================
# DIRECTION VECTORS (for neighbor calculation)
# ============================================================================
DIRECTIONS = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1),   # Right
]
