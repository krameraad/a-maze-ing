import sys
import random
from enum import IntEnum
from dataclasses import dataclass


class Dir(IntEnum):
    N = 0b1110
    E = 0b1101
    S = 0b1011
    W = 0b0111


@dataclass
class Maze:
    """Maze structure and generation logic."""
    width: int = 15
    height: int = 15
    entry: tuple[int, int] = (0, 0)
    exit: tuple[int, int] = (14, 14)
    perfect: bool = False
    seed: int = 0
    pattern: list[str] | None = None

    def __post_init__(self) -> None:
        # Validate arguments.
        if self.width <= 1:
            raise ValueError("Maze width invalid, must be more than 1")
        if self.height <= 1:
            raise ValueError("Maze height invalid, must be more than 1")
        x, y = self.entry
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise ValueError("Entry coordinates are out of bounds.")
        x, y = self.exit
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise ValueError("Exit coordinates are out of bounds.")
        if self.entry == self.exit:
            raise ValueError("Entry and exit share coordinates.")

        self.logo = self.get_pattern_cells(self.pattern)
        if self.entry in self.logo or self.exit in self.logo:
            raise ValueError("Entry or exit overlap with the 42 pattern.")

        # Create grid of cells.
        self.grid: list[list[int]] = []
        for y in range(self.height):
            current_row = []
            for x in range(self.width):
                current_row.append(0b1111)
            self.grid.append(current_row)

        self.generate()

    def generate(self) -> None:
        """Generate the maze layout."""
        if self.seed != 0:
            random.seed(self.seed)

        # Close all cells.
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 0b1111

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
            (0, +1): Dir.N,
            (-1, 0): Dir.E,
            (0, -1): Dir.S,
            (+1, 0): Dir.W}

        x, y = current[0] - neighbor[0], current[1] - neighbor[1]
        self.grid[current[1]][current[0]] &= DIRECTIONS[(x, y)]
        self.grid[neighbor[1]][neighbor[0]] &= DIRECTIONS[(-x, -y)]

    def _open_dead_ends(self) -> None:
        """Make all eligible dead-ends into straight corridors."""
        # Which dead-end orientation corresponds to which direction.
        DIRECTIONS = {
            Dir.N: (0, +1),  # Opening is north, target is south
            Dir.E: (-1, 0),  # Opening is east, target is west
            Dir.S: (0, -1),  # Opening is south, target is north
            Dir.W: (+1, 0)}  # Opening is west, target is east

        for y in range(self.height):
            for x in range(self.width):
                # Check that we're dealing with any of the dead-end variants.
                if self.grid[y][x] not in DIRECTIONS:
                    continue
                direction = DIRECTIONS[Dir(self.grid[y][x])]
                nx, ny = (direction[0] + x, direction[1] + y)  # Target cell.
                # Validate that the target is within the maze bounds,
                # and that the target is not part of the logo.
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and (nx, ny) not in self.logo:
                    self._carve_passage((x, y), (nx, ny))

    def get_pattern_cells(self, pattern: list[str] | None = None
                          ) -> set[tuple[int, int]]:
        """Return set of cells that form an arbitrary pattern
        in the center of the maze."""
        if pattern is None:
            pattern = [
                "         ",
                " # # ### ",
                " # #   # ",
                " ### ### ",
                "   # #   ",
                "   # ### ",
                "         "]
        cells: set[tuple[int, int]] = set()

        # Maze should be big enough to contain the pattern.
        LOGO_W, LOGO_H = len(max(pattern)), len(pattern)
        if self.width < LOGO_W or self.height < LOGO_H:
            print(f"Maze too small for pattern "
                  f"(minimum {LOGO_W}x{LOGO_H}, "
                  f"got {self.width}x{self.height}).",
                  file=sys.stderr)
            return cells

        offset_x = self.width // 2 - LOGO_W // 2
        offset_y = self.height // 2 - LOGO_H // 2
        for y, row in enumerate(pattern):
            for x, char in enumerate(row):
                if char == '#':
                    cells.add((x + offset_x, y + offset_y))

        return cells
