# PathFinding Visualizer

An interactive visualization tool for popular pathfinding algorithms built with Python and PyGame. Watch how BFS, DFS, Dijkstra, and A* explore a grid to find the shortest path between two points.

## What It Does

This visualizer lets you see exactly how different pathfinding algorithms work. You can place start and end points, draw walls, or generate random mazes, then watch as the algorithm searches for a path. Each algorithm has its own approach and trade-offs, which become really clear when you see them side-by-side.

## Features

**Four Classic Algorithms:**
- **BFS** - Explores layer by layer, guarantees shortest path
- **DFS** - Goes deep first, doesn't guarantee shortest path
- **Dijkstra** - Like BFS but handles weighted paths
- **A\*** - Uses heuristics to find paths faster than Dijkstra

**Interactive Controls:**
- Draw walls by clicking and dragging
- Generate random mazes with one keypress
- Adjust animation speed on the fly
- See real-time stats (time, nodes visited, path length)

**Visual Feedback:**
- Color-coded nodes show algorithm progress
- Gradient effect shows visit order
- Clean UI with live statistics

## How to Use

**Setup:**
```bash
git clone https://github.com/ParjanyaReddy/PathfindingVisualizer.git
cd PathfindingVisualizer
pip install -r requirements.txt
python main.py
```

**Controls:**
- First click: Place start node (orange)
- Second click: Place end node (turquoise)  
- Click and drag: Draw walls
- Right click: Erase nodes
- **SPACE**: Run the algorithm
- **C**: Clear everything
- **R**: Generate random maze
- **1-4**: Switch algorithms
- **+/-**: Adjust speed

## Project Structure

```
PathfindingVisualizer/
├── algorithms/        # Each algorithm in its own file
├── main.py           # Main game loop and event handling
├── grid.py           # Grid data structure
├── node.py           # Individual node logic
├── renderer.py       # Drawing and visualization
└── constants.py      # Colors, sizes, settings
```

The code is organized with separation of concerns - algorithms are isolated from rendering, making it easy to add new ones or modify the UI independently.

## How It Works

Each algorithm is implemented as a generator that yields after visiting each node. This lets the main loop update the display in real-time without blocking. The grid tracks node states, and the renderer handles all PyGame drawing.

**Algorithm Comparison:**

| Algorithm | Shortest Path? | Speed | Best For |
|-----------|---------------|-------|----------|
| BFS | Yes | Medium | Unweighted graphs |
| DFS | No | Fast | Exploring all paths |
| Dijkstra | Yes | Slower | Weighted graphs |
| A* | Yes | Fastest | When you know the goal |

## Technical Details

- Built with PyGame for rendering and event handling
- Generator-based algorithm implementation for smooth animation
- Object-oriented design with clear separation between grid logic and visualization
- Type hints throughout for better code clarity

## What I Learned

This project helped me understand:
- How different pathfinding algorithms actually work under the hood
- The trade-offs between completeness, optimality, and speed
- Working with PyGame's event loop and rendering
- Implementing algorithms as generators for step-by-step visualization

## Future Ideas

Some things I might add:
- Bidirectional search
- Jump Point Search for faster pathfinding
- More maze generation algorithms
- Ability to save/load grids
- Weighted nodes to better show Dijkstra vs A*

## License

MIT License - feel free to use this for learning or your own projects.

---

Built with Python and PyGame. Inspired by similar visualizers but implemented from scratch to learn the algorithms deeply.
