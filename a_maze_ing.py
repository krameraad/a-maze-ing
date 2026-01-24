from enum import Enum

Vector = tuple[int, int]


class Dir(Enum):
    """Enum of directions (N, E, S, W)."""
    N = 0b0001
    E = 0b0010
    S = 0b0100
    W = 0b1000


WALL_GLYPHS = {
    # Key : Glyph  : Wall positions
    0b0000: '┼',   # none

    0b0001: '┬',   # north
    0b0010: '┤',   # east
    0b0100: '┴',   # south
    0b1000: '├',   # west

    0b0101: '─',   # north + south
    0b1010: '│',   # east + west

    0b0011: '┐',   # north + east
    0b0110: '┘',   # east + south
    0b1100: '└',   # south + west
    0b1001: '┌',   # west + north

    0b0111: '╴',   # north + east + south
    0b1110: '╵',   # east + south + west
    0b1101: '╶',   # south + west + north
    0b1011: '╷',   # west + north + east

    0b1111: ' ',   # all
}

# WALL_GLYPHS = {
#     0b0000: '┼',   # ! none

#     0b0001: '╵',   # north
#     0b0010: '╶',   # east
#     0b0100: '╷',   # south
#     0b1000: '╴',   # west

#     0b0101: '─',   # ! east + west
#     0b1010: '│',   # ! north + south

#     0b0011: '└',   # north + east
#     0b0110: '┌',   # east + south
#     0b0011: '┐',   # ! south + west
#     0b1001: '┘',   # west + north

#     0b0111: '├',   # north + east + south
#     0b1110: '┬',   # east + south + west
#     0b1101: '┤',   # south + west + north
#     0b1011: '┴',   # west + north + east

#     0b1111: ' ',   # ! all
# }


class Maze:
    """
    Represents a maze with an entry and exit point inside of it.
    The maze can optionally be perfect, having only
    a single route to the exit.

    Args:
        size (Vector): Width and height of the maze.
        entry (Vector): Position of the maze's entry point.
        exit (Vector): Position of the maze's exit point.
        output (str): Name of the output file.
        perfect (bool): Whether the maze should be perfect or not.
    """
    def __init__(
            self,
            size: Vector,
            entry: Vector,
            exit: Vector,
            output="maze.txt",
            perfect=False
            ):
        self.__size = size
        self.__entry = entry
        self.__exit = exit
        self.__output = output
        self.__perfect = perfect

    class MazeError(Exception):
        pass

    class Cell:
        """
        Single cell as part of a maze.

        Args:
            walls (int): Four-bit flags representing \
                which walls of the cell are open.
        """
        def __init__(self, walls=0b1111):
            self.walls = walls

        def __str__(self):
            return "♥"

    def tunnel(self, start: Cell, end: Cell) -> Cell:
        """
        Open walls to connect the cells `start` and `end`.
        If the cells aren't next to eachother, raises `MazeError`.

        Args:
            start (Cell): Start of the tunnel.
            end (Cell): Destination of the tunnel.

        Returns:
            Cell: The cell that the newly made tunnel ends in.
        """
        pass

    def generate(self):
        self.test_cell = Maze.Cell()


if __name__ == "__main__":
    maze = Maze((20, 20), (3, 3), (17, 17))
    maze.generate()
    print(maze.test_cell)
