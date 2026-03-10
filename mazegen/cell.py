from typing import Final


class Cell:
    """Represents a maze cell with four walls.

    Each wall is True if closed, False if open.
    """
    WALLMAP: Final = {
        "N": 0b0001,
        "E": 0b0010,
        "S": 0b0100,
        "W": 0b1000}
    "Mapping of directions (NESW) to wall configurations in binary."

    def __init__(self) -> None:
        self.walls = 0b1111

    def open_wall(self, direction: str) -> None:
        "Open a wall in a direction, using one of N, E, S or W."
        self.walls &= 0b1111 - self.WALLMAP[direction.upper()]

    def has_wall(self, direction: str) -> bool:
        "Check if a wall exists in a direction, using one of N, E, S or W."
        return bool(self.walls & self.WALLMAP[direction.upper()])
