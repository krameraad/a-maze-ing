from typing import List
from collections import deque
from maze import Maze


class MazeSolver:
    """Find shortest path inside maze."""

    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    # --------------------------------------------------

    def solve(self) -> List[str]:
        """Return path as list of 'N','E','S','W'."""

        start = self.maze.entry
        end = self.maze.exit

        queue = deque([start])
        came_from = {start: None}

        while queue:
            current = queue.popleft()

            if current == end:
                break

            x, y = current
            cell = self.maze.grid[y][x]

            directions = {
                "N": (x, y - 1),
                "E": (x + 1, y),
                "S": (x, y + 1),
                "W": (x - 1, y),
            }

            for direction, (nx, ny) in directions.items():
                x_is_valid = nx >= 0 and nx < self.maze.width
                y_is_valid = ny >= 0 and ny < self.maze.height
                if x_is_valid and y_is_valid:
                    # Only move if there is NO wall
                    if not cell.has_wall(direction):
                        if (nx, ny) not in came_from:
                            queue.append((nx, ny))
                            came_from[(nx, ny)] = (current, direction)

        # Reconstruct path
        path: List[str] = []
        current = end

        while came_from[current] is not None:
            previous, direction = came_from[current]
            path.append(direction)
            current = previous

        path.reverse()
        return path
