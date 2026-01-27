import os
import sys


def interface() -> int:
    print("0: Exit program\n"
          "1: Regenerate the maze\n"
          "2: Toggle path to the exit\n"
          "3: Change maze colors\n")
    match input("Select an option: "):
        case "0":
            sys.exit()
        case "1":
            return 1
        case "2":
            return 2
        case "3":
            return 3
        case _:
            input("\033[91mInvalid option, press enter to try again\033[0;m")
            os.system("cls" if os.name == "nt" else "clear")
    return 0


if __name__ == "__main__":
    while True:
        option = interface()
        if option:
            print(option)
