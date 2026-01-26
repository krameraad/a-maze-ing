from .maze import Maze
from .get_config import get_config

if __name__ == "__main__":
    maze = Maze((5, 5), (3, 3), (4, 4))
    maze.generate()
    print(maze)
    maze.create_output()
    get_config("config.txt")
    # print(maze.cells[0][0].__walls)

    # print(repr(Maze.Cell(Maze.Cell.CType.ENTRY, 0b0011)))
