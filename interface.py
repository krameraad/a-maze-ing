import os
import sys


def interface() -> int:
    """
    Display options for the user and forward the results to the program.

    - `0`: Exits the program (handled in function).
    - `1`: Regenerate the maze.
    - `2`: Toggle path to the exit.
    - `3`: Change the maze colors.
    - `default`: Returns `0` (invalid input).

    Returns:
        int: Option selected by the user, which is either 0, 1, 2 or 3.
    """
    print("\033[1;93m0\033[0m: Exit program\n"
          "\033[1;93m1\033[0m: Regenerate maze\n"
          "\033[1;93m2\033[0m: Toggle path to the exit\n"
          "\033[1;93m3\033[0m: Change maze colors\n")
    match input("Select an option: "):
        case "0":
            sys.exit()
        case "1":
            return 1
        case "2":
            return 2
        case "3":
            return 3
    return 0


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    msg = "\033[1;93mWelcome to A-Maze-ing!\033[0m"
    while True:
        print(msg)
        print("\n\033[2m<Maze>\033[0m\n")
        match interface():
            case 1:
                msg = "\033[2mRegenerated maze.\033[0m"
            case 2:
                msg = "\033[2mToggled path.\033[0m"
            case 3:
                msg = "\033[2mChanged maze colors.\033[0m"
            case _:
                msg = "\033[91mInvalid option, try again.\033[0;m"
        os.system("cls" if os.name == "nt" else "clear")
