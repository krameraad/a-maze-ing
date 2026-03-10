import os
import random
from typing import Any
from mlx import Mlx

from mazegen.maze import Maze


class RenderError(Exception):
    pass


class Context:
    """Holds all data relevant across rendering."""
    def __init__(self, maze: Maze) -> None:
        self.m = Mlx()
        "The MLX class itself."
        self.p = self.m.mlx_init()
        "Pointer to the MLX connection."
        self.gfx: dict[str, Any] = {}
        """Dictionary of all loaded images. `gfx` means graphics.
        Images are of type `Any` and the key for each image is
        its filepath inside the assets folder."""
        self.win: Any = None
        "Window to render in."
        self.maze = maze
        "Maze data."
        self.scale = 64
        "Size of a tile (could be 32 or 64 pixels)."


def load_assets(ctx: Context, dir: str) -> None:
    """Load all assets from a directory, including its subdirectories."""
    for x in os.listdir(dir):
        file = f"{dir}/{x}"
        if os.path.isdir(file):
            load_assets(ctx, file)
        else:
            name = file.removeprefix("assets/").removesuffix(".png")
            ctx.gfx.update(
                {name: ctx.m.mlx_png_file_to_image(ctx.p, file)[0]})
            if not ctx.gfx[name]:
                raise RenderError(f"failed loading PNG from {file}")


def render(maze: Maze, path: list[str]) -> bool:
    """Render the maze using MLX.

    Args:
        maze: Maze to render.
        path: Path from the entry to the exit.

    Returns:
        bool: Whether to regenerate the maze after the loop exits.

    Raises:
        RenderError: When the assets fail to load.
        ValueError: If the path contains invalid characters."""
    ctx = Context(maze)
    load_assets(ctx, "assets")

    regenerate = False  # Whether to regenerate the maze after ending the loop.
    path_visible = False

    # Setting correct scale ---------------------------------------------------
    w, h = ctx.m.mlx_get_screen_size(ctx.p)[1:]  # Discard first element (Any).
    if maze.width * ctx.scale > w or maze.height * ctx.scale > h:
        ctx.scale = 32
    # After setting the scale, we use `w` and `h` to store the window size.
    w, h = ctx.scale * ctx.maze.width, max(ctx.scale * ctx.maze.height, 512)

    # Colors ------------------------------------------------------------------
    colors = ["red", "green", "blue", "cyan", "pink", "yellow"]
    color_i = random.randint(0, 5)  # Index of the currently used color.

    # Render helpers ----------------------------------------------------------
    def create_window() -> None:
        """Create a window and render the buttons inside."""
        ctx.win = ctx.m.mlx_new_window(
                    ctx.p,
                    w + 256,
                    h,
                    "A-Maze-ing")
        ctx.m.mlx_clear_window(ctx.p, ctx.win)

        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win, ctx.gfx["button/regenerate"], w, 0)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win, ctx.gfx["button/color"], w, 128)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win, ctx.gfx["button/path"], w, 256)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win, ctx.gfx["button/exit"], w, 384)
        ctx.m.mlx_do_sync(ctx.p)

    def render_maze_cells(subdir: str) -> None:
        """Render the backgrounds for the cells, the cells themselves,
        and the entry and exit."""
        ctx.m.mlx_do_sync(ctx.p)  # Reduces chance of corruption.
        for y, row in enumerate(maze.grid):
            ctx.m.mlx_do_sync(ctx.p)  # Reduces chance of corruption.
            for x, cell in enumerate(row):
                # Draw a colored background for the cell.
                ctx.m.mlx_put_image_to_window(
                    ctx.p, ctx.win,
                    ctx.gfx[f"{subdir}color/{colors[color_i]}"],
                    x * ctx.scale,
                    y * ctx.scale)

                # Draw the cell itself.
                ctx.m.mlx_put_image_to_window(
                    ctx.p,
                    ctx.win,
                    ctx.gfx[f"{subdir}{cell.walls:04b}"],
                    x * ctx.scale,
                    y * ctx.scale)

        x, y = maze.entry[0] * ctx.scale, maze.entry[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win,
            ctx.gfx[f"{subdir}obj/entry"], x, y)

        x, y = maze.exit[0] * ctx.scale, maze.exit[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win,
            ctx.gfx[f"{subdir}obj/exit"], x, y)

    def render_path(subdir: str) -> None:
        """Render the path to the exit."""
        ctx.m.mlx_do_sync(ctx.p)  # Reduces chance of corruption.
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
            ctx.m.mlx_put_image_to_window(
                ctx.p,
                ctx.win,
                ctx.gfx[f"{subdir}path"],
                x * ctx.scale,
                y * ctx.scale)
            ctx.m.mlx_do_sync(ctx.p)

    # Hooks -------------------------------------------------------------------
    def on_mouse(button: int, x: int, y: int, params: Any) -> None:
        nonlocal regenerate, color_i, path_visible
        if x < ctx.scale * ctx.maze.width:  # Check if inside sidebar.
            return

        if y < 127:  # Regenerate button.
            regenerate = True
            ctx.m.mlx_destroy_window(ctx.p, ctx.win)
            ctx.m.mlx_loop_exit(ctx.p)

        elif 127 < y < 255:  # Color button.
            color_i = (color_i + 1) % len(colors)
            render_maze_cells(f"tile{ctx.scale}/")
            if path_visible:
                render_path(f"tile{ctx.scale}/obj/")
            ctx.m.mlx_do_sync(ctx.p)

        elif 255 < y < 384:  # Path button.
            if path_visible:
                render_maze_cells(f"tile{ctx.scale}/")
                path_visible = False
            else:
                render_path(f"tile{ctx.scale}/obj/")
                path_visible = True
            ctx.m.mlx_do_sync(ctx.p)

        elif 384 < y < 512:  # Exit button.
            ctx.m.mlx_loop_exit(ctx.p)

    def on_key(keynum: int, params: Any) -> None:
        if keynum == 65307:
            ctx.m.mlx_loop_exit(ctx.p)

    def on_close(dummy: Any) -> None:
        ctx.m.mlx_loop_exit(ctx.p)

    # Environment and initial render ------------------------------------------
    create_window()
    render_maze_cells(f"tile{ctx.scale}/")
    ctx.m.mlx_do_sync(ctx.p)

    # Setting up hooks --------------------------------------------------------
    ctx.m.mlx_mouse_hook(ctx.win, on_mouse, None)
    ctx.m.mlx_key_hook(ctx.win, on_key, None)
    ctx.m.mlx_hook(ctx.win, 33, 0, on_close, None)

    ctx.m.mlx_loop(ctx.p)
    return regenerate
