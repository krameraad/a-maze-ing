def get_config(file: str) -> tuple:
    with open(file) as f:
        buffer = f.read().splitlines()
        i = buffer.index("WIDTH")
        j = buffer[i].index("=")
        print(buffer[i][j:])
    return (0, 0)
