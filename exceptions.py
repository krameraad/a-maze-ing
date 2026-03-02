# flake8: noqa

class MazeError(Exception):
    pass


class ConfigError(MazeError):
    def __init__(self, message: str="Error With the Config file ❌❌❌") -> None:
        super().__init__(message)


class MazeGenerationError(MazeError):
    def __init__(self, message: str="Problem generation the maze with that size") -> None:
        super().__init__(message)


class MazeValidationError(MazeError):
    def __init__(self, msge: str="Not a valid instruction for generating the Maze") -> None:
        super().__init__(msge)
