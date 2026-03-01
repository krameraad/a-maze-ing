from pathlib import Path
from typing import List
from maze import Maze


def write_maze(
    maze: Maze,
    path: List[str],
    output_path: Path,
) -> None:
    """Write maze to file using required format."""

    with output_path.open("w") as f:
        # Write maze grid as hex
        for row in maze.grid:
            line = ""
            for cell in row:
                hex_value = cell.to_hex()
                line = line + hex_value
            f.write(line + "\n")
        f.write("\n")

        # Write entry and exit
        ex, ey = maze.entry
        fx, fy = maze.exit
        f.write(f"{ex},{ey}\n")
        f.write(f"{fx},{fy}\n")

        # Write shortest path
        f.write("".join(path) + "\n")
