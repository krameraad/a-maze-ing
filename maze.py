import random
from typing import List, Tuple
from cell import Cell
from config import Config


class Maze:
    """Maze structure and generation logic."""

    def __init__(self, config: Config) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit

        # Create grid with all walls closed
        self.grid = []

        for row in range(self.height):
            current_row = []
            for col in range(self.width):
                new_cell = Cell(True, True, True, True)
                current_row.append(new_cell)
            self.grid.append(current_row)

    # --------------------------------------------------

    def generate_perfect(self) -> None:
        """Generate perfect maze."""
        self._generate_perfect()

    def generate_non_perfect_maze(self) -> None:
        """Generate NON perfect maze"""
        self._generate_perfect()
        self._add_loops(loop_factor=0.15)

    # --------------------------------------------------

    def _neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Return valid neighbor coordinates."""
        neighbors = []

        directions = [
            (x, y - 1),  # North
            (x + 1, y),  # East
            (x, y + 1),  # South
            (x - 1, y),  # West
        ]

        for nx, ny in directions:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))

        return neighbors

    # --------------------------------------------------

    def _carve_passage(
        self,
        current: Tuple[int, int],
        neighbor: Tuple[int, int],
    ) -> None:
        """Remove walls between two adjacent cells."""

        x1, y1 = current
        x2, y2 = neighbor

        cell1 = self.grid[y1][x1]
        cell2 = self.grid[y2][x2]

        if x2 == x1 and y2 == y1 - 1:  # North
            cell1.open_wall("N")
            cell2.open_wall("S")

        elif x2 == x1 + 1 and y2 == y1:  # East
            cell1.open_wall("E")
            cell2.open_wall("W")

        elif x2 == x1 and y2 == y1 + 1:  # South
            cell1.open_wall("S")
            cell2.open_wall("N")

        elif x2 == x1 - 1 and y2 == y1:  # West
            cell1.open_wall("W")
            cell2.open_wall("E")

    # --------------------------------------------------

    def _wall_exists(
        self,
        current: Tuple[int, int],
        neighbor: Tuple[int, int],
    ) -> bool:

        x1, y1 = current
        x2, y2 = neighbor

        cell = self.grid[y1][x1]

        if x2 == x1 and y2 == y1 - 1:
            return cell.has_wall("N")

        elif x2 == x1 + 1 and y2 == y1:
            return cell.has_wall("E")

        elif x2 == x1 and y2 == y1 + 1:
            return cell.has_wall("S")

        elif x2 == x1 - 1 and y2 == y1:
            return cell.has_wall("W")

        return False

    # ----------------------------------------------------

    def _generate_perfect(self) -> None:
        """Generate perfect maze using DFS backtracking."""

        visited = set()
        stack = []

        start = (0, 0)
        stack.append(start)
        visited.add(start)

        while stack:
            current = stack[-1]
            x, y = current

            # Get unvisited neighbors

            unvisited = []
            for nx, ny in self._neighbors(x, y):
                if (nx, ny) not in visited:
                    unvisited.append((nx, ny))
            # unvisited = [
            #     (nx, ny)
            #     for nx, ny in self._neighbors(x, y)
            #     if (nx, ny) not in visited
            # ]

            if unvisited:
                neighbor = random.choice(unvisited)

                self._carve_passage(current, neighbor)

                visited.add(neighbor)
                stack.append(neighbor)
            else:
                stack.pop()
    # ------------------------------------------------------

    def _add_loops(self, loop_factor=0.15):
        walls = []

        for y in range(self.height):
            for x in range(self.width):
                for nx, ny in self._neighbors(x, y):
                    # Only consider East and South to avoid duplicates
                    if nx > x or ny > y:
                        if self._wall_exists((x, y), (nx, ny)):
                            walls.append(((x, y), (nx, ny)))

        random.shuffle(walls)

        loops_to_add = int(len(walls) * loop_factor)

        for i in range(loops_to_add):
            self._carve_passage(*walls[i])

    # ------------------------------------------------------

    def shortest_path(self) -> List[str]:
        """Return shortest path from entry to exit using NSEW."""

        from collections import deque

        queue = deque()
        queue.append(self.entry)

        came_from = {self.entry: None}

        while queue:
            current = queue.popleft()

            if current == self.exit:
                break

            x, y = current
            cell = self.grid[y][x]

            directions = {
                "N": (x, y - 1),
                "E": (x + 1, y),
                "S": (x, y + 1),
                "W": (x - 1, y),
            }

            for direction, (nx, ny) in directions.items():
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not cell.has_wall(direction):
                        if (nx, ny) not in came_from:
                            queue.append((nx, ny))
                            came_from[(nx, ny)] = (current, direction)

        # Reconstruct path
        if self.exit not in came_from:
            return []

        path = []
        current = self.exit

        while came_from[current] is not None:
            previous, direction = came_from[current]
            path.append(direction)
            current = previous

        path.reverse()
        return path
