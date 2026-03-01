import sys
from pathlib import Path

from config import parse_config
from maze import Maze
from solver import MazeSolver
from writer import write_maze
from exceptions import MazeError
from render import render, RenderError
import audio


def main() -> None:
    """Main entry point for the A-Maze-ing program."""

    print("Welcome To OUR Maze Generator! 🚪")

    # Check command-line arguments --------------------------------------------
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    config_file = Path(sys.argv[1])

    if not config_file.exists():
        print(f"Error: Config file not found: {config_file}")
        sys.exit(1)

    regenerate = True
    while regenerate:
        # Parse configuration -------------------------------------------------
        try:
            config = parse_config(config_file)
        except Exception as e:
            print(f"Error parsing config: {e}")
            sys.exit(1)
        except ValueError:
            print("You can only enter '1'! STUPID 👿👿👿")

        # Generate maze -------------------------------------------------------
        try:
            maze = Maze(config)
            if config.perfect:
                maze.generate_perfect()
            else:
                maze.generate_non_perfect_maze()
        except MazeError as e:
            print(f"Maze generation error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error during maze generation: {e}")
            sys.exit(1)

        # Solve maze for shortest path ----------------------------------------
        try:
            solver = MazeSolver(maze)
            path = solver.solve()
        except Exception as e:
            print(f"Error solving maze: {e}")
            sys.exit(1)

        # Write maze to output file -------------------------------------------
        try:
            output_path = Path(config.output_file)
            write_maze(maze, path, output_path)
            print(f"Maze successfully written to {output_path}")
        except Exception as e:
            print(f"Error writing maze: {e}")
            sys.exit(1)

        audio.init_audio()
        audio.play_music("kakaist-cinematic-hit-3-317170.mp3")
        try:
            regenerate = render(maze, path)
        except (ValueError, RenderError) as e:
            print("Error rendering maze:", e)
            sys.exit(1)


if __name__ == "__main__":
    main()
