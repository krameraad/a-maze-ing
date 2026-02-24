class MazeError(Exception):
    pass


class ConfigError(MazeError):
    def __init__(self, message="Error With the Config file ❌❌❌"):
        super().__init__(message)


class MazeGenerationError(MazeError):
    def __init__(self, message="Not able to find the file"):
        super().__init__(message)


class MazeValidationError(MazeError):
    def __init__(self, msge="Not a valid instruction for generating the Maze"):
        super().__init__(msge)
