from pathlib import Path
from typing import List

from mazegen.maze import Maze


def write_maze(
    maze: Maze,
    path: List[str],
    output_path: Path,
) -> None:
    """Write maze to file using required format."""

    with output_path.open("w") as f:
        # Write maze grid as hex
        out = ""
        for row in maze.grid:
            for cell in row:
                out += f"{cell.get_walls():X}"
            out += "\n"
        f.write(out + "\n")

        # Write entry and exit
        ex, ey = maze.entry
        fx, fy = maze.exit
        f.write(f"{ex},{ey}\n")
        f.write(f"{fx},{fy}\n")

        # Write shortest path
        f.write("".join(path) + "\n")
