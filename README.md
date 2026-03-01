*This project has been created as part of the 42 curriculum by rulouis and ekramer*


# A-Maze-ing
[![preview.jpg](https://i.postimg.cc/Hs1rWHNs/preview.jpg)](https://postimg.cc/s1KjwFyt)

A graphical maze generator and viewer.

A-Maze-ing is the first project to test us not only on applied Python skills,
but also teamwork, considering it's the first group project.
The program consists of multiple important steps, including:
- Reading and parsing a config file
- Implementing an algorithm to create and traverse a graph
- Displaying information using a simple graphics library (optional)
- Exporting a reusable module


## Instructions
### Configuration
The project directory contains a file named **config.txt**.
Each line in this file determines some aspect of the maze.
```
# Width and height of the maze.
WIDTH=20
HEIGHT=20

# Entry and exit, expressed as 2D coordinates.
ENTRY=0,0
EXIT=19,19

# Name of the output file.
OUTPUT_FILE=maze.txt

# Whether the maze should be perfect or not.
PERFECT=True

# Mazes generated with the same seed will have the same layout.
# Can be left out of the file to generate a random seed on program start.
SEED=42
```

### Install and run
The program requires the MiniLibX library to be run.
Download the `mlx_CLXV` file from Intra, unpack it, then run `make` inside.
This produces a `.whl` file that can be installed with `pip`.

To install other dependencies and run the program, execute these commands:
```bash
make install
make run
```
A window opens with the generated maze, and an additional window contains
options for interacting with it.
Close the program by clicking `Exit`, pressing `ESC` or by closing any window.
- **Regenerate**: Generate the maze again, with a new layout if no **seed** was given.
- **Color**: Cycle through 6 colors for the maze walls.
- **Path**: Toggle a visible path from the start to the end.
- **Exit**: Close the program.


## Resources
As with most projects, a lot of help was acquired through
[GeeksforGeeks](https://www.geeksforgeeks.org/), [W3Schools](https://www.w3schools.com/),
random YouTube videos and AI chats. Of course, other students were also very helpful.
In particular, Wikipedia was useful this time to explain more high-level
graph theory concepts like **spanning trees**.

Some time ago, I (*ekramer*) watched [this video](https://youtu.be/184Oair5iys)
on maze generation algorithms in Minecraft. I found it very interesting,
but it was before I really took programming seriously.
When discovering we were doing a maze project at Codam,
I went back to the video and learned so much.
It was very helpful during this project, introducing a lot of algorithms
and general concepts about mazes.

In addition, me and *rulouis* read a book during this project, called
[Grokking Algorithms](https://www.manning.com/books/grokking-algorithms-second-edition).
It contained a lot of helpful information and even Python code snippets,
all about algorithms. The book just so happened to discuss precisely the algorithms we needed
in this project, like **depth-first-search**.


## Additional info
This project includes a reusable module, stripped down to the maze structure
and its generation algorithm. This is in preparation for a later project,
where a fully-fledged game will be made.

Two algorithms are important for this project: **depth-first-** and **breadth-first-search**
(DFS and BFS).
The first traverses branches of a graph fully, before returning to the root.
The second traverses the nodes closest to the root first, while slowly expanding outwards.
They are very similar in implementation, but have different applications:
DFS is useful for creating long, random branches, as with generating a maze.
BFS is used to find the shortest path, perfect for finding the exit.

***rulouis*** was responsible for implementing these important algorithms
(generating and solving the maze), applying the 42 logo, and parsing configuration.

***ekramer*** also worked on parsing, and made the Maze and Cell classes,
drew the graphics, implemented the MLX rendering and wrote this readme.

We both had a lot of overlapping work as well.
For the parts only one person was responsible for,
we still both collaborated using brainstorming and discussion.
It took some time to really get started on the project,
and we had to drop some ideas (like multiple algorithms) for the sake of time.
In the end we got together and worked hard to make a strong impression.
