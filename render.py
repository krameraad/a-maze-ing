import os
import random
from typing import Any
from mlx import Mlx

from mazegen.maze import Maze
from solver import solve_maze


class RenderError(Exception):
    pass


def render(maze: Maze, path: list[str]) -> None:
    """Render the maze using MLX.

    Args:
        maze: Maze to render.
        path: Path from the entry to the exit.

    Returns:
        bool: Whether to regenerate the maze after the loop exits.

    Raises:
        RenderError: When the assets fail to load.
        ValueError: If the path contains invalid characters."""

    # Render helpers ----------------------------------------------------------
    def load_assets(dir: str) -> dict[str, Any]:
        """Load all assets from a directory, including its subdirectories.

        Args:
            dir: Directory to load from.

        Returns:
            Dictionary of all loaded images.
            Images are of type `Any` and the key for each image is
            its filepath inside the assets folder."""
        result = {}
        for x in os.listdir(dir):
            file = f"{dir}/{x}"
            if os.path.isdir(file):
                result.update(load_assets(file))
            else:
                name = file.removeprefix("assets/").removesuffix(".png")
                result.update(
                    {name: m.mlx_png_file_to_image(p, file)[0]})
                if not result[name]:
                    raise RenderError(f"failed loading PNG from {file}")
        return result

    def get_scale() -> int:
        "Get the ideal tilesize for displaying the maze (32 or 64)."
        w, h = m.mlx_get_screen_size(p)[1:]
        if maze.width * 64 > w or maze.height * 64 > h:
            return 32
        return 64

    def create_window(width: int, height: int) -> Any:
        "Create a window and render the buttons inside."
        window = m.mlx_new_window(p, width + 256,
                                  height, "A-Maze-ing")
        m.mlx_clear_window(p, window)

        m.mlx_put_image_to_window(
            p, window, gfx["button/regenerate"], width, 0)
        m.mlx_put_image_to_window(
            p, window, gfx["button/color"], width, 128)
        m.mlx_put_image_to_window(
            p, window, gfx["button/path"], width, 256)
        m.mlx_put_image_to_window(
            p, window, gfx["button/exit"], width, 384)
        m.mlx_do_sync(p)

        return window

    def render_maze_cells() -> None:
        """Render the backgrounds for the cells, the cells themselves,
        and the entry and exit."""
        m.mlx_do_sync(p)  # Reduces chance of corruption.
        for y, row in enumerate(maze.grid):
            m.mlx_do_sync(p)  # Reduces chance of corruption.
            for x, cell in enumerate(row):
                # Draw a colored background for the cell.
                m.mlx_put_image_to_window(
                    p, win,
                    gfx[f"tile{scale}/color/{colors[color_i]}"],
                    x * scale,
                    y * scale)

                # Draw the cell itself.
                m.mlx_put_image_to_window(
                    p,
                    win,
                    gfx[f"tile{scale}/{cell.walls:04b}"],
                    x * scale,
                    y * scale)

        x, y = maze.entry[0] * scale, maze.entry[1] * scale
        m.mlx_put_image_to_window(
            p,
            win,
            gfx[f"tile{scale}/obj/entry"], x, y)
        x, y = maze.exit[0] * scale, maze.exit[1] * scale
        m.mlx_put_image_to_window(
            p,
            win,
            gfx[f"tile{scale}/obj/exit"], x, y)

        m.mlx_do_sync(p)

    def render_path() -> None:
        "Render the path to the exit."
        m.mlx_do_sync(p)  # Reduces chance of corruption.
        x, y = maze.entry
        # Everything but the last element; we don't want to draw over the exit.
        for char in path[:-1]:
            match char:
                case 'N':
                    y -= 1
                case 'E':
                    x += 1
                case 'S':
                    y += 1
                case 'W':
                    x -= 1
                case _:
                    raise ValueError("path contains invalid character")
            m.mlx_put_image_to_window(
                p,
                win,
                gfx[f"tile{scale}/obj/path"],
                x * scale,
                y * scale)
            m.mlx_do_sync(p)

    # Basic setup -------------------------------------------------------------
    m = Mlx()  # The MLX object itself.
    p = m.mlx_init()  # Pointer to the MLX connection.
    gfx = load_assets("assets")  # `gfx` means graphics.
    scale = get_scale()  # Size of a tile (could be 32 or 64 pixels).
    win = create_window(scale * maze.width, max(scale * maze.height, 512))
    colors = ["red", "green", "blue", "cyan", "pink", "yellow"]
    color_i = random.randint(0, 5)  # Index of the currently used color.
    path_visible = False

    # Hooks -------------------------------------------------------------------
    def hook_setup() -> None:
        m.mlx_mouse_hook(win, on_mouse, None)
        m.mlx_key_hook(win, on_key, None)
        m.mlx_hook(win, 33, 0, on_close, None)

    def on_mouse(button: int, x: int, y: int, params: Any) -> None:
        nonlocal path, scale, win, color_i, path_visible
        if x < scale * maze.width:  # Check if inside sidebar.
            return

        if y < 127:  # Regenerate button.
            maze.generate()
            path = solve_maze(maze)
            scale = get_scale()
            m.mlx_destroy_window(p, win)
            win = create_window(scale * maze.width,
                                max(scale * maze.height, 512))
            hook_setup()
            color_i = (color_i + 1) % len(colors)
            render_maze_cells()
            if path_visible:
                render_path()

        elif 127 < y < 255:  # Color button.
            color_i = (color_i + 1) % len(colors)
            render_maze_cells()
            if path_visible:
                render_path()

        elif 255 < y < 384:  # Path button.
            if path_visible:
                render_maze_cells()
                path_visible = False
            else:
                render_path()
                path_visible = True

        elif 384 < y < 512:  # Exit button.
            m.mlx_loop_exit(p)

    def on_key(keynum: int, params: Any) -> None:
        if keynum == 65307:
            m.mlx_loop_exit(p)

    def on_close(dummy: Any) -> None:
        m.mlx_loop_exit(p)

    hook_setup()
    render_maze_cells()

    m.mlx_loop(p)
