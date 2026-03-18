import sys
from pathlib import Path


from mazegen.maze import Maze
from config import parse_config, ConfigError
from solver import solve_maze
from writer import write_maze
from render import render, RenderError


print("\033[1mWelcome to A-Maze-ing!\033[0m")

# Check command-line arguments ------------------------------------------------
if len(sys.argv) != 2:
    print("Usage: python3 a_maze_ing.py config.txt")
    sys.exit(1)

# Parse configuration ---------------------------------------------------------
try:
    config = parse_config(Path(sys.argv[1]))
except ConfigError as e:
    print(f"Config error: {e}")
    sys.exit(1)

# Generate maze ---------------------------------------------------------------
try:
    maze = Maze(*config[:4], *config[5:])
except ValueError as e:
    print(f"Maze generation error: {e}")
    sys.exit(1)

# Solve maze for shortest path ------------------------------------------------
try:
    path = solve_maze(maze)
except Exception as e:
    print(f"Error solving maze: {e}")
    sys.exit(1)

# Write maze to output file ---------------------------------------------------
try:
    output_path = Path(config[4])
    write_maze(maze, path, output_path)
    print(f"Maze successfully written to {output_path}")
except Exception as e:
    print(f"Error writing maze: {e}")
    sys.exit(1)

try:
    render(maze, path)
except (RenderError, ValueError) as e:
    print("Error rendering maze:", e)
    sys.exit(1)
