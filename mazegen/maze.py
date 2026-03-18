import sys
import random

from mazegen.cell import Cell


class Maze:
    """Maze structure and generation logic."""
    def __init__(
            self,
            width: int = 15,
            height: int = 15,
            entry: tuple[int, int] = (0, 0),
            exit: tuple[int, int] = (14, 14),
            perfect: bool = False,
            seed: int = 0
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

        # Validate and correct arguments.
        if self.width <= 1:
            raise ValueError("Maze width invalid, must be more than 1")
        if self.height <= 1:
            raise ValueError("Maze height invalid, must be more than 1")
        x, y = self.entry
        if not 0 <= x < width or not 0 <= y < height:
            raise ValueError("Entry coordinates are out of bounds.")
        x, y = self.exit
        if not 0 <= x < width or not 0 <= y < height:
            raise ValueError("Exit coordinates are out of bounds.")
        if self.entry == self.exit:
            raise ValueError("Entry and exit share coordinates.")

        self.logo = self._logo_cells()
        if self.entry in self.logo or self.exit in self.logo:
            raise ValueError("Entry or exit overlap with the 42 pattern.")

        # Create grid of cells.
        self.grid: list[list[Cell]] = []
        for y in range(self.height):
            current_row = []
            for x in range(self.width):
                current_row.append(Cell())
            self.grid.append(current_row)

        self.generate()

    def __repr__(self) -> str:
        return f"Maze({self.width=}, " \
               f"{self.height=}, " \
               f"{self.entry=}, " \
               f"{self.exit=}, " \
               f"{self.perfect=}, " \
               f"{self.seed=}" \
                ")".replace("self.", "")

    def generate(self) -> None:
        """Generate the maze layout."""
        if self.seed != 0:
            random.seed(self.seed)

        # Close all cells.
        for row in self.grid:
            for cell in row:
                cell.walls = 0b1111

        visited = {(0, 0)}
        stack = [(0, 0)]

        while stack:
            current = stack[-1]
            x, y = current
            # Get unvisited neighbors
            unvisited = []
            for nx, ny in self._neighbors(x, y):
                if (nx, ny) not in visited and (nx, ny) not in self.logo:
                    unvisited.append((nx, ny))

            if unvisited:
                neighbor = random.choice(unvisited)
                self._carve_passage(current, neighbor)
                visited.add(neighbor)
                stack.append(neighbor)
            else:
                stack.pop()

        if not self.perfect:
            self._open_dead_ends()

    def _neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return valid neighbor coordinates."""
        neighbors = []

        directions = [
            (x, y - 1),  # North
            (x + 1, y),  # East
            (x, y + 1),  # South
            (x - 1, y)]  # West

        for nx, ny in directions:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))

        return neighbors

    def _carve_passage(
        self,
        current: tuple[int, int],
        neighbor: tuple[int, int],
    ) -> None:
        """Remove walls between two adjacent cells."""
        DIRECTIONS = {
            (0, +1): 0b1110,
            (-1, 0): 0b1101,
            (0, -1): 0b1011,
            (+1, 0): 0b0111}

        x, y = current[0] - neighbor[0], current[1] - neighbor[1]
        self.grid[current[1]][current[0]].walls &= DIRECTIONS[(x, y)]
        self.grid[neighbor[1]][neighbor[0]].walls &= DIRECTIONS[(-x, -y)]

    def _open_dead_ends(self) -> None:
        """Make all eligible dead-ends into straight corridors."""
        # Which dead-end orientation corresponds to which direction.
        DIRECTIONS = {
            0b1110: (0, +1),  # Opening is north, target is south
            0b1101: (-1, 0),  # Opening is east, target is west
            0b1011: (0, -1),  # Opening is south, target is north
            0b0111: (+1, 0)}  # Opening is west, target is east

        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                # Check that we're dealing with any of the dead-end variants.
                if cell.walls not in DIRECTIONS:
                    continue
                direction = DIRECTIONS[cell.walls]
                nx, ny = (direction[0] + x, direction[1] + y)  # Target cell.
                # Validate that the target is within the maze bounds,
                # and that the target is not part of the logo.
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and (nx, ny) not in self.logo:
                    self._carve_passage((x, y), (nx, ny))

    def _logo_cells(self) -> set[tuple[int, int]]:
        """Return cells that form the '42' logo in the center of the maze."""
        cells: set[tuple[int, int]] = set()

        # Maze should be big enough to contain the logo.
        MIN_WIDTH, MIN_HEIGHT = 9, 7
        if self.width < MIN_WIDTH or self.height < MIN_HEIGHT:
            print(f"Maze too small for '42' logo "
                  f"(minimum {MIN_WIDTH}x{MIN_HEIGHT}, "
                  f"got {self.width}x{self.height}).",
                  file=sys.stderr)
            return cells

        # Pixel art pattern for "42" (relative offsets from center-left)
        # Each tuple is (col_offset, row_offset) from anchor point
        fourtytwo = [
            (0, 0), (0, 1), (0, 2),          # left vertical
                    (1, 2), (2, 2),          # horizontal bar
                    (2, 0), (2, 1), (2, 3), (2, 4),  # right vertical

            (4, 0), (5, 0), (6, 0),          # top bar
                            (6, 1),          # top-right
            (4, 2), (5, 2), (6, 2),          # middle bar
            (4, 3),                          # bottom-left
            (4, 4), (5, 4), (6, 4),          # bottom bar
        ]

        offset_x = self.width // 2 - 3
        offset_y = self.height // 2 - 2
        for x, y in fourtytwo:
            cells.add((x + offset_x, y + offset_y))

        return cells
