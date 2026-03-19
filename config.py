from pathlib import Path
from typing import Any


class ConfigError(Exception):
    pass


def parse_bool(value: str, key: str) -> bool:
    """Parse boolean value from string."""
    if value == "True":
        return True
    if value == "False":
        return False
    raise ConfigError(f"{key} must be 'True' or 'False' (got {value})")


def parse_coordinates(value: str, key: str) -> tuple[int, int]:
    """Parse coordinate string 'x,y'."""
    try:
        x_str, y_str = value.split(",", maxsplit=1)
        return int(x_str), int(y_str)
    except ValueError as e:
        raise ConfigError(
            f"{key} must be in format x,y with integers (got {value})") from e


def parse_int(value: str, key: str) -> int:
    """Convert a string to int safely."""
    try:
        return int(value)
    except ValueError as e:
        raise ConfigError(f"{key} must be an integer (got {value})") from e


def parse_config(file_path: Path) -> dict[str, Any]:
    """Parse and validate a maze configuration file.

    Args:
        file_path: Path to the configuration file.

    Returns:
        Dictionary containing all keyword arguments for a maze.

    Raises:
        ConfigError: If the configuration file is invalid.
    """
    data: dict[str, str] = {}
    result: dict[str, Any] = {}

    try:
        with file_path.open("r", encoding="utf-8") as file:
            for i, raw_line in enumerate(file, start=1):
                line = raw_line.strip()

                # Ignore empty lines and comments
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ConfigError(f"Invalid line format at line {i}.")

                key, value = line.split("=", maxsplit=1)
                data[key.strip()] = value.strip()
    except FileNotFoundError as e:
        raise ConfigError(f"Couldn't find file '{file_path}'") from e

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
    result["width"] = parse_int(data["WIDTH"], "WIDTH")
    result["height"] = parse_int(data["HEIGHT"], "HEIGHT")
    result["entry"] = parse_coordinates(data["ENTRY"], "ENTRY")
    result["exit"] = parse_coordinates(data["EXIT"], "EXIT")
    result["perfect"] = parse_bool(data["PERFECT"], "PERFECT")
    result["seed"] = parse_int(data.get("SEED", "0"), "SEED")
    result["output_file"] = data["OUTPUT_FILE"]

    pattern_file = data.get("PATTERN")
    if not pattern_file:
        return result
    try:
        with Path("patterns/" + pattern_file).open("r") as file:
            result["pattern"] = [x for x in file.read().splitlines()]
    except FileNotFoundError as e:
        raise ConfigError(f"Couldn't find file '{pattern_file}'") from e
    return result
