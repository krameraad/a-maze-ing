import maze_algorithms as algorithms  # noqa
# from .maze import Maze
from collections.abc import Callable
from enum import Enum

Vector = tuple[int, int]


class Maze:
    """
    Represents a maze with an entry and exit point inside of it.
    The maze can optionally be perfect, having only
    a single route to the exit.

    When initialized, the maze does not have a layout yet.
    Use `.generate()` to create the layout or to
    regenerate a layout before displaying the maze.

    Args:
        size (Vector): Width and height of the maze.
        entry (Vector): Position of the maze's entry point.
        exit (Vector): Position of the maze's exit point.
        output (str): Name of the output file.
        perfect (bool): Whether the maze should be perfect or not.
    """
    class Dir(Enum):
        """Enum of directions (N, E, S, W)."""
        N = 0b0001
        E = 0b0010
        S = 0b0100
        W = 0b1000

    class MazeError(Exception):
        """Captures exceptions specific to mazes."""
        pass

    class Cell:
        """
        Single cell as part of a maze.

        Args:
            ctype (CType): Represents the type of this cell.
            walls (int): Four-bit flags representing \
                which walls of the cell are open.
        """
        class CType(Enum):
            DEFAULT = 0
            ENTRY = 1
            EXIT = 2
            PATTERN = 3

        __glyphs = {
            # Key : Glyph  : Wall positions
            0b0000: '┼─',   # none

            0b0001: '┬─',   # north
            0b0010: '┤ ',   # east
            0b0100: '┴─',   # south
            0b1000: '├─',   # west

            0b0101: '──',   # north + south
            0b1010: '│ ',   # east + west

            0b0011: '╮ ',   # north + east
            0b0110: '╯ ',   # east + south
            0b1100: '╰─',   # south + west
            0b1001: '╭─',   # west + north

            0b0111: '╴ ',   # north + east + south
            0b1110: '╵ ',   # east + south + west
            0b1101: '╶─',   # south + west + north
            0b1011: '╷ ',   # west + north + east

            0b1111: '░░',   # all
        }

        def __init__(self, ctype=CType.DEFAULT, walls=0b1111):
            self.__ctype = ctype
            self.__walls = walls

        def set_ctype(self, ctype: CType) -> None:
            if ctype in self.CType:
                self.__ctype = ctype
            else:
                raise Maze.MazeError("tried to set invalid ctype")

        def __int__(self) -> int:
            return self.__walls

        def __str__(self) -> str:
            match self.__ctype:
                case self.CType.ENTRY:
                    return "\033[96m<>\033[0m"  # Cyan
                case self.CType.EXIT:
                    return "\033[95m[]\033[0m"  # Magenta
                case self.CType.PATTERN:
                    return "\033[91m██\033[0m"  # Red
            return self.__glyphs[self.__walls]

        def __repr__(self) -> str:
            return "Maze.Cell(" \
                   f"ctype=Maze.Cell.{self.__ctype}, " \
                   f"walls=0b{self.__walls:04b})"

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

    def generate(self, algorithm: Callable[[list], None]) -> None:
        """Generate the layout of the maze."""
        self.cells: list[list[Maze.Cell]] = []
        for y in range(self.__size[0]):
            row = []
            for x in range(self.__size[1]):
                row.append(Maze.Cell(walls=0b1111))
            self.cells.append(row)
        x, y = self.__entry
        self.cells[x][y].set_ctype(Maze.Cell.CType.ENTRY)
        x, y = self.__exit
        self.cells[x][y].set_ctype(Maze.Cell.CType.EXIT)
        if algorithm:
            algorithm(self.cells)

    def to_hex(self) -> str:
        result = ""
        for row in self.cells:
            for cell in row:
                result += hex(int(cell)).removeprefix("0x").upper()
            result += "\n"
        with open(self.__output, "w") as f:
            f.write(result + "\n")
            s = str(self.__entry[0]) + "," + str(self.__entry[1])
            f.write(s + "\n")
            s = str(self.__exit[0]) + "," + str(self.__exit[1])
            f.write(s + "\n")
        return result

    def __str__(self) -> str:
        result = ""
        for row in self.cells:
            for cell in row:
                result += str(cell)
            result += "\n"
        return result


if __name__ == "__main__":
    maze = Maze((5, 5), (3, 3), (4, 4))
    maze.generate(algorithms.binary_tree)
    print(maze)
    maze.to_hex()
    # print(maze.cells[0][0].__walls)

    print(repr(Maze.Cell(Maze.Cell.CType.ENTRY, 0b0011)))
