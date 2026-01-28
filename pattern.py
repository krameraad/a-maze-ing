from typing import Optional

DEFAULT = "         \n" \
          " #   ### \n" \
          " #     # \n" \
          " ### ### \n" \
          "   # #   \n" \
          "   # ### \n" \
          "         "


def draw_pattern(pattern: Optional[str]) -> None:
    if not pattern:
        pattern = DEFAULT
    pattern = pattern.splitlines()
    x, y = 0, 0
    for row in pattern:
        for char in row:
            # make cell [x][y] "PATTERN" type
            # but only if char is '#'
            x += 1
        y += 1
