ConfigInfo = tuple[tuple[int, int],
                   tuple[int, int],
                   tuple[int, int],
                   str,
                   bool]


def find_value(lines: list[str], query: str) -> tuple[str, int]:
    for line in lines:
        if query in line:
            return (line, line.index("=") + 1)
    raise KeyError(f"no config entry for {query}")


def get_config(file: str) -> ConfigInfo:
    width = 20
    height = 20
    entry = (3, 3)
    exit = (17, 17)
    output = "maze.txt"
    perfect = False

    with open(file) as f:
        buf = f.read().splitlines()

        line, index = find_value(buf, "WIDTH")
        width = int(line[index:])
        if width < 2 or width > 100:
            raise ValueError(f"width {width} invalid; must be from 2 to 100")

        line, index = find_value(buf, "HEIGHT")
        height = int(line[index:])
        if height < 2 or height > 100:
            raise ValueError(f"height {height} invalid; must be from 2 to 100")

        line, index = find_value(buf, "ENTRY")
        entry = line[index:].split(",")
        entry = (int(entry[0]), int(entry[1]))
        if entry[0] < 0 or entry[0] > width \
           or entry[1] < 0 or entry[1] > height:
            raise ValueError(f"entry {entry} outside of maze bounds")

        line, index = find_value(buf, "EXIT")
        exit = line[index:].split(",")
        exit = (int(exit[0]), int(exit[1]))
        if exit[0] < 0 or exit[0] > width \
           or exit[1] < 0 or exit[1] > height:
            raise ValueError(f"exit {exit} outside of maze bounds")

        if entry == exit:
            raise ValueError(f"entry and exit at same position {entry}")

        line, index = find_value(buf, "OUTPUT_FILE")
        output = line[index:]
        if not len(output):
            raise ValueError("output file name empty")

        line, index = find_value(buf, "PERFECT")
        perfect = "True" in line[index:]

    return ((width, height), entry, exit, output, perfect)
