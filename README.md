# 🗺️ PathFinding Visualizer

A professional-grade **interactive pathfinding algorithm visualizer** built with Python and PyGame. Visualize how popular graph traversal and pathfinding algorithms explore a grid to find the shortest path between two points.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyGame](https://img.shields.io/badge/PyGame-2.5.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Features

### 🔍 **4 Pathfinding Algorithms**
- **BFS (Breadth-First Search)** - Guarantees shortest path (unweighted)
- **DFS (Depth-First Search)** - Explores deeply before backtracking
- **Dijkstra's Algorithm** - Shortest path with weighted edges
- **A\* (A-Star)** - Optimal pathfinding with heuristic optimization

### 🎨 **Interactive Visualization**
- **Real-time Animation** - Watch algorithms explore the grid step-by-step
- **Adjustable Speed** - Control animation speed with `+` and `-` keys
- **Color-Coded States** - Distinct colors for visited, path, barriers, etc.
- **Performance Stats** - Track time, nodes visited, and path length

### 🧱 **Maze Generation**
- **Recursive Backtracker** - Generate random, solvable mazes instantly
- **Custom Walls** - Draw your own barriers with mouse drag

### 📊 **Professional UI**
- **Live Statistics Panel** - Algorithm name, execution time, visited nodes, path length
- **Gradient Visualization** - Nodes fade based on visit order
- **Smooth Animations** - Polished visual experience

---

## 🎮 Controls

| Key/Mouse | Action |
|-----------|--------|
| **Left Click (1st)** | Place Start Node (Orange) |
| **Left Click (2nd)** | Place End Node (Turquoise) |
| **Left Click + Drag** | Draw Walls (Black) |
| **Right Click** | Erase Node |
| **SPACE** | Start Pathfinding |
| **C** | Clear Board |
| **R** | Generate Random Maze |
| **1** | Select BFS Algorithm |
| **2** | Select DFS Algorithm |
| **3** | Select Dijkstra Algorithm |
| **4** | Select A* Algorithm (Default) |
| **+** | Increase Animation Speed |
| **-** | Decrease Animation Speed |
| **ESC** | Cancel/Quit |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/PathfindingVisualizer.git
   cd PathfindingVisualizer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

---

## 📁 Project Structure

```
PathfindingVisualizer/
├── algorithms/
│   ├── __init__.py          # Algorithm exports
│   ├── astar.py             # A* implementation
│   ├── bfs.py               # BFS implementation
│   ├── dfs.py               # DFS implementation
│   ├── dijkstra.py          # Dijkstra implementation
│   └── maze.py              # Maze generation
├── constants.py             # Configuration & colors
├── grid.py                  # Grid data structure
├── node.py                  # Node class with state management
├── renderer.py              # PyGame rendering engine
├── main.py                  # Application entry point
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

---

## 🎯 How It Works

### Algorithm Flow
1. **Place Start & End** - Click to set starting and ending points
2. **Draw Barriers** (Optional) - Create obstacles or generate a maze
3. **Select Algorithm** - Choose from BFS, DFS, Dijkstra, or A*
4. **Visualize** - Press SPACE to watch the algorithm in action
5. **Analyze** - Review performance stats and path efficiency

### Color Legend
- 🟧 **Orange** - Start Node
- 🟦 **Turquoise** - End Node
- ⬛ **Black** - Barrier/Wall
- 🟩 **Green** - Visited Node (gradient based on order)
- 🟪 **Purple** - Final Path
- ⬜ **White** - Unvisited Node

---

## 🧠 Algorithm Comparison

| Algorithm | Guarantees Shortest Path | Time Complexity | Space Complexity | Best Use Case |
|-----------|--------------------------|-----------------|------------------|---------------|
| **BFS** | ✅ Yes (unweighted) | O(V + E) | O(V) | Unweighted graphs |
| **DFS** | ❌ No | O(V + E) | O(V) | Maze solving, backtracking |
| **Dijkstra** | ✅ Yes (weighted) | O((V + E) log V) | O(V) | Weighted graphs |
| **A*** | ✅ Yes (with admissible heuristic) | O(E) | O(V) | Optimal pathfinding |

---

## 🛠️ Technical Highlights

- **Object-Oriented Design** - Clean separation of concerns (Grid, Node, Renderer)
- **Generator-Based Algorithms** - Yield-based animation for smooth visualization
- **Event-Driven Architecture** - Responsive PyGame event handling
- **Performance Optimized** - Efficient data structures and rendering
- **Type Hints** - Full Python type annotations for code clarity
- **Modular Codebase** - Easy to extend with new algorithms

---

## 📈 Future Enhancements

- [ ] Bidirectional search algorithms
- [ ] Jump Point Search (JPS)
- [ ] More maze generation algorithms (Prim's, Kruskal's)
- [ ] Save/Load grid configurations
- [ ] Weighted nodes for Dijkstra/A*
- [ ] Export visualization as GIF/video

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Built with [PyGame](https://www.pygame.org/)
- Inspired by classic pathfinding visualizers
- Algorithms based on standard computer science implementations

---

## 📸 Screenshots

*Add screenshots of your visualizer in action here!*

---

**⭐ If you found this project helpful, please consider giving it a star!**
