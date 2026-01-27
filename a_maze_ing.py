from maze import Maze
from get_config import get_config
from algorithms.binary_tree import binary_tree

if __name__ == "__main__":
    try:
        config = get_config()
        print("Config:", config, "\n")
        maze = Maze(*config)
    except (KeyError, ValueError) as e:
        print(f"\033[91mInvalid config file: {e}\033[0m\n")
        maze = Maze()
    maze.generate(binary_tree)
    print(maze)
    maze.create_output()

    print(repr(Maze.Cell(Maze.Cell.CType.ENTRY, 0b0011)))
    print(repr(maze))
