from dataclasses import dataclass


@dataclass
class Cell:
    """Represents a maze cell with four walls.

    Each wall is True if closed, False if open.
    """

    north: bool = True
    east: bool = True
    south: bool = True
    west: bool = True

    def to_hex(self) -> str:
        """Convert wall configuration to hexadecimal digit.

        Returns:
            A single hexadecimal character representing the walls.
        """
        value: int = 0

        if self.north:
            value |= 1  # 0001
        if self.east:
            value |= 2  # 0010
        if self.south:
            value |= 4  # 0100
        if self.west:
            value |= 8  # 1000

        return format(value, "X")

    def close_wall(self, direction: str) -> None:
        """Close the wall in the given direction.

        Args:
            direction: One of 'N', 'E', 'S', 'W'.
        """
        direction = direction.upper()

        if direction == "N":
            self.north = True
        elif direction == "E":
            self.east = True
        elif direction == "S":
            self.south = True
        elif direction == "W":
            self.west = True
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def open_wall(self, direction: str) -> None:
        """Open the wall in the given direction.

        Args:
            direction: One of 'N', 'E', 'S', 'W'.
        """
        direction = direction.upper()

        if direction == "N":
            self.north = False
        elif direction == "E":
            self.east = False
        elif direction == "S":
            self.south = False
        elif direction == "W":
            self.west = False
        else:
            raise ValueError(f"Invalid direction: {direction}")

    def has_wall(self, direction: str) -> bool:
        """Check whether a wall exists in a direction.

        Args:
            direction: One of 'N', 'E', 'S', 'W'.

        Returns:
            True if wall is closed, False if open.
        """
        direction = direction.upper()

        if direction == "N":
            return self.north
        if direction == "E":
            return self.east
        if direction == "S":
            return self.south
        if direction == "W":
            return self.west

        raise ValueError(f"Invalid direction: {direction}")
