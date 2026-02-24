from pathlib import Path
from typing import Optional, Tuple, Dict
from exceptions import ConfigError
import random


class Config:
    """Represents validated maze configuration."""

    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: Path
    perfect: bool
    seed: Optional[int]

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        output_file: Path,
        perfect: bool,
        seed: Optional[int] = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.output_file = output_file
        self.perfect = perfect
        self.seed = seed


def parse_bool(value: str) -> bool:
    """Parse boolean value from string."""
    if value == "True":
        return True
    if value == "False":
        return False

    raise ConfigError("PERFECT must be True or False.")


def parse_coordinates(value: str, key: str) -> Tuple[int, int]:
    """Parse coordinate string 'x,y'."""
    try:
        x_str, y_str = value.split(",", maxsplit=1)
        return int(x_str), int(y_str)
    except ValueError as error:
        raise ConfigError(
            f"{key} must be in format x,y with integers."
        ) from error


def parse_int(value: str, key: str) -> int:
    """Convert a string to int safely."""
    try:
        return int(value)
    except ValueError as error:
        raise ConfigError(f"{key} must be an integer.") from error


def validate_coordinates(
    coord: Tuple[int, int],
    width: int,
    height: int,
    key: str,
) -> None:
    """Ensure coordinates are inside maze bounds."""
    x, y = coord

    if x < 0 or x >= width or y < 0 or y >= height:
        raise ConfigError("Coordinates are out of bounds.")


def parse_config(file_path: Path) -> Config:
    """Parse and validate a maze configuration file.

    Args:
        file_path: Path to the configuration file.

    Returns:
        A validated Config object.

    Raises:
        ConfigError: If the configuration file is invalid.
    """

    if not file_path.exists() or not file_path.is_file():
        raise ConfigError(f"Config file not found: {file_path}")

    data: Dict[str, str] = {}

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(
                        f"Invalid line format at line {line_number}."
                    )

                key, value = line.split("=", maxsplit=1)
                key = key.strip()
                value = value.strip()

                data[key] = value
    except ConfigError as error:
        raise ConfigError(f"Error reading configuration file: {error}") \
            from error

    # Validate required keys
    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = required_keys - data.keys()
    if missing:
        raise ConfigError(f"Missing required keys: {', '.join(missing)}")

    # Convert types safely
    width = parse_int(data["WIDTH"], "WIDTH")
    height = parse_int(data["HEIGHT"], "HEIGHT")
    entry = parse_coordinates(data["ENTRY"], "ENTRY")
    exit_ = parse_coordinates(data["EXIT"], "EXIT")
    perfect = parse_bool(data["PERFECT"])
    output_file = Path(data["OUTPUT_FILE"])

    if width <= 0 or height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers.")

    # Validate bounds
    validate_coordinates(entry, width, height, "ENTRY")
    validate_coordinates(exit_, width, height, "EXIT")

    if entry == exit_:
        raise ConfigError("ENTRY and EXIT must be different.")

    seed: Optional[int] = None
    if "SEED" in data:
        seed = parse_int(data["SEED"], "SEED")
        if seed != 0:
            random.seed(seed)

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
