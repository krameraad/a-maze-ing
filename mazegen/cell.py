from dataclasses import dataclass


@dataclass
class Cell:
    """Represents a maze cell with four walls.

    Each wall is True if closed, False if open.
    """
    walls = 0b1111
