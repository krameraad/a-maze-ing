import random
from typing import List, Tuple
from cell import Cell
from config import Config
from exceptions import MazeGenerationError


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
        self._apply_logo()

    def generate_non_perfect_maze(self) -> None:
        """Generate NON perfect maze"""
        self._generate_perfect()
        self._add_loops(loop_factor=0.10)
        self._apply_logo()

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

        logo = self._logo_cells()
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
                if (nx, ny) not in visited and (nx, ny) not in logo:
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

    def _add_loops(self, loop_factor=0.10):
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

    # ------------------------------------------------------
    # 42 LOGO
    def _logo_cells(self) -> set:
        """Return cells that form the '42' logo in the center of the maze."""
        cx = self.width // 2
        cy = self.height // 2

        # Pixel art pattern for "42" (relative offsets from center-left)
        # Each tuple is (col_offset, row_offset) from anchor point
        four = [
            (0, 0), (0, 1), (0, 2),          # left vertical
                    (1, 2), (2, 2),    # horizontal bar
                    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),  # right vertical
        ]
        two = [
            (4, 0), (5, 0), (6, 0),          # top bar
                            (6, 1),          # top-right
            (4, 2), (5, 2), (6, 2),          # middle bar
            (4, 3),                      # bottom-left
            (4, 4), (5, 4), (6, 4),          # bottom bar
        ]

        anchor_col = cx - 3  # shift left to center the whole "42"
        anchor_row = cy - 2  # shift up to center vertically

        cells = set()
        for dc, dr in four + two:
            col = anchor_col + dc
            row = anchor_row + dr
            if 0 <= col < self.width and 0 <= row < self.height:
                cells.add((col, row))

        return cells

    def _apply_logo(self) -> None:
        """Re-wall all logo cells to form '42' in the center."""

        MIN_WIDTH = 12
        MIN_HEIGHT = 7

        if self.width < MIN_WIDTH or self.height < MIN_HEIGHT:
            raise MazeGenerationError(
                f"Maze too small for '42' logo"
                f"(minimum {MIN_WIDTH}x{MIN_HEIGHT}, "
                f"got {self.width}x{self.height})."
            )

        logo = self._logo_cells()

        # Check BEFORE discarding
        if self.entry in logo:
            raise MazeGenerationError(
                f"Entry point {self.entry} "
                f"conflicts with the '42' logo position."
            )
        if self.exit in logo:
            raise MazeGenerationError(
                f"Exit point {self.exit} "
                f"conflicts with the '42' logo position."
            )

        # Now safe to proceed
        protected = set()
        protected.add(self.entry)
        protected.add(self.exit)
        for pos in [self.entry, self.exit]:
            x, y = pos
            for nx, ny in self._neighbors(x, y):
                protected.add((nx, ny))

        logo -= protected

        for (x, y) in logo:
            cell = self.grid[y][x]
            cell.close_wall("N")
            cell.close_wall("E")
            cell.close_wall("S")
            cell.close_wall("W")

            for direction, (nx, ny), opposite in [
                ("N", (x, y-1), "S"),
                ("E", (x+1, y), "W"),
                ("S", (x, y+1), "N"),
                ("W", (x-1, y), "E"),
            ]:
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in logo:
                        self.grid[ny][nx].close_wall(opposite)
