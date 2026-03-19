from typing import List, Any
from collections import deque

from mazegen.maze import Maze, Dir


def solve_maze(maze: Maze) -> List[str]:
    """Return path as list of 'N','E','S','W'."""

    start = maze.entry
    end = maze.exit

    queue = deque([start])
    came_from: dict[tuple[int, int], Any] = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            break

        x, y = current
        cell = maze.grid[y][x]

        directions = {
            "N": (x, y - 1),
            "E": (x + 1, y),
            "S": (x, y + 1),
            "W": (x - 1, y),
        }

        for direction, (nx, ny) in directions.items():
            x_is_valid = nx >= 0 and nx < maze.width
            y_is_valid = ny >= 0 and ny < maze.height
            if x_is_valid and y_is_valid:
                # Only move if there is NO wall
                if not cell & (0b1111 - Dir[direction]):
                    if (nx, ny) not in came_from:
                        queue.append((nx, ny))
                        came_from[(nx, ny)] = (current, direction)

    # Reconstruct path
    path: List[str] = []
    current = end
    if end not in came_from:
        print("No path found - exit is unreachable.")
        return []

    while came_from[current] is not None:
        previous, direction = came_from[current]
        path.append(direction)
        current = previous

    path.reverse()
    return path
