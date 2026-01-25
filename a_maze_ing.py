import maze_algorithms as algorithms  # noqa
from .maze import Maze

if __name__ == "__main__":
    maze = Maze((20, 20), (3, 3), (17, 17))
    maze.generate(algorithms.binary_tree)
    print(maze)

    print(repr(Maze.Cell(Maze.Cell.CType.ENTRY, 0b0011)))
