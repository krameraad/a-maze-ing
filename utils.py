from enum import Enum


class Dir(Enum):
    """Enum of directions (N, E, S, W)."""
    N = 0b0001
    E = 0b0010
    S = 0b0100
    W = 0b1000


class MazeError(Exception):
    """Captures exceptions specific to mazes."""
    pass


# def tunnel(self, start: Maze.Cell, end: Maze.Cell) -> None:
#     """
#     Open walls to connect the cells `start` and `end`.
#     If the cells aren't next to eachother, raises `MazeError`.

#     Args:
#         start (Cell): Start of the tunnel.
#         end (Cell): Destination of the tunnel.

#     Returns:
#         Cell: The cell that the newly made tunnel ends in.
#     """
#     start.__walls = 0b0011
#     end.__walls = 0b1100
