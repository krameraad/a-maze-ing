# import queue
# from pathlib import Path

# def create_maze() -> list:
#     maze = []
#     maze.append(["#", "#", "#", "o", "#", "#", "#", "#", "#"])
#     maze.append(["#", " ", " ", " ", "#", " ", " ", "#", "#"])
#     maze.append(["#", " ", "#", " ", "#", " ", "#", " ", "#"])
#     maze.append(["#"," " ,"#"," ", " "," ","#", " ", "#"])
#     maze.append(["#"," " ,"#","#", "#"," ","#", "#", "#"])
#     maze.append(["#"," " ," "," ", "#"," "," ", " ", "#"])
#     maze.append(["#","x" ,"#","#", "#","#","#", "#", "#"])
#     return maze


# def print_maze(maze, path=""):
#     for x, posi in enumerate(maze[0]):
#         if posi == 'o':
#             start = x

#     i = start
#     j = 0
#     posi = set()
#     for move in path:
#         if move == 'L':
#             i -= 1
#         elif move == 'R':
#             i += 1
#         elif move == 'U':
#             j -= 1
#         elif move == 'D':
#             j += 1
#         posi.add((j, i))

#     for j, row in enumerate(maze):
#         for i, colu in enumerate(row):
#             if (j, i) in posi:
#                 print("+", end="")
#             else:
#                 print(colu + " ", end="")
#         print()


# def valid(maze, moves) -> bool:
#     for x, posi in enumerate(maze[0]):
#         if posi == 'o':
#             start = x

#     i = start
#     j = 0
#     for move in moves:
#         if move == 'L':
#             i -= 1
#         elif move == 'R':
#             i += 1
#         elif move == 'U':
#             j -= 1

#         elif move == 'D':
#             j += 1
#         if not (0 <= i < len(maze[0]) and 0 <= j < len(maze)):
#             return False
#         elif maze[j][i] == "#":
#             return False
#     return True


# def find_end(maze, moves):
#     for x, posi in enumerate(maze[0]):
#         if posi == 'o':
#             start = x

#     i = start
#     j = 0
#     for move in moves:
#         if move == 'L':
#             i -= 1
#         elif move == 'R':
#             i += 1
#         elif move == 'U':
#             j -= 1

#         elif move == 'D':
#             j += 1
#         if maze[j][i] == "x":
#             print(f"Found: {moves}")
#             print_maze(maze, moves)
#             return True
#     return False


# if __name__ == "__main__":

#     nums = queue.Queue()
#     nums.put("")
#     add = ""
#     maze = create_maze()
#     while not find_end(maze, add):
#         add = nums.get()
#         for j in ["L", "R", "U", "D"]:
#             put = add + j
#             if valid(maze, put):
#                 nums.put(put)


# print(Path("maze.txt").resolve())
