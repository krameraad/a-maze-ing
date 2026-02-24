from typing import List
from maze import Maze


def display_ascii(maze: Maze, path: List[str] = []) -> None:
    """Print human-readable ASCII maze to console."""

    width = maze.width
    height = maze.height
    grid = maze.grid

    # Build set of path coordinates
    path_cells = set()
    x, y = maze.entry
    path_cells.add((x, y))
    for move in path:
        if move == "N":
            y -= 1
        elif move == "S":
            y += 1
        elif move == "E":
            x += 1
        elif move == "W":
            x -= 1
        path_cells.add((x, y))

    # Top border
    print("+" + "---+" * width)

    for row_y in range(height):
        row_top = "|"
        row_bottom = "+"

        for row_x in range(width):
            cell = grid[row_y][row_x]

            # Cell content
            if (row_x, row_y) == maze.entry:
                content = " E "
            elif (row_x, row_y) == maze.exit:
                content = " X "
            elif (row_x, row_y) in path_cells:
                content = " O "
            else:
                content = "   "

            row_top += content

            # East wall
            # East wall — check if neighbor is also on path
            if cell.east:
                if (row_x, row_y) in path_cells and (row_x + 1, row_y) in path_cells:
                    row_top += " "  # just open space instead of · on the wall
                else:
                    row_top += "|"
            else:
                row_top += " "

            # South wall
            if cell.south:
                if (row_x, row_y) in path_cells and (row_x, row_y + 1) in path_cells:
                    row_bottom += " O +"
                else:
                    row_bottom += "---+"
            else:
                row_bottom += "   +"

        print(row_top)
        print(row_bottom)
