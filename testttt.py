# import networkx as nx
# import matplotlib.pyplot as plt

# graph = {
#          5: (3, 7),
#          3: (2, 4),
#          7: (8,),
#          2: (),
#          4: (8,),
#          8: ()
#          }

# visited: list = []
# queu: list = []

# class Bfs():
#     def __init__(self, visited: list, graph: dict[str, any], node):
#         self.visited = visited
#         self.graph = graph
#         self.node = node

#         visited.append(node)
#         queu.append(node)
#         while queu:
#             buffer = queu.pop(0)
#             print(buffer)
#             for neighbor in graph[buffer]:
#                 if neighbor not in visited:
#                     visited.append(neighbor)
#                     queu.append(neighbor)

# new = Bfs(visited, graph, 5)
# G = nx.DiGraph()

# for node, neighbors in graph.items():
#     for neighbor in neighbors:
#         G.add_edge(node, neighbor)

# # Color visited nodes
# colors = []
# for node in G.nodes():
#     if node in visited:
#         colors.append("lightblue")
#     else:
#         colors.append("white")

# nx.draw(G, with_labels=True, node_color=colors, node_size=1000, font_size=16, arrows=True)
# plt.title("BFS Graph")
# plt.show()

# for _ in range(3):
#     for _ in range(4):
#         print("[ ]", end="")
#     print()

# def create_grid(width: int, height: int) -> list:
#     grid = []
#     for row in range(height):
#         current_row = []
#         for col in range(width):
#             current_row.append(" ")
#         grid.append(current_row)
#     return grid

# def print_grid(grid: list) -> None:
#     width = len(grid[0])
#     print("+" + "---+" * width)
#     for row in grid:
#         print("|", end="")
#         for cell in row:
#             print(f" {cell} |", end="")
#         print()
#         print("+" + "---+" * width)

# grid = create_grid(4, 4)
# print_grid(grid)

def shrink(name: str) -> str:
    i = 0
    buffer = ""
    for i, letter in enumerate(name):
        if i != 9:
            buffer += letter
        else:
            break
    return buffer



print(shrink("Louishhfjj"))