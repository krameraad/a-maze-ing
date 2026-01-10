class MazeGenerator:
    class Cell:
        def __init__(self, walls=[True, True, True, True]):
            self.walls = walls
