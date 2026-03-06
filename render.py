import os
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
        self.win: list[Any] = []
        "All our created windows."
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

    # Colors ------------------------------------------------------------------
    colors = ["red", "green", "blue", "cyan", "pink", "yellow"]
    color_i = 0  # Index of the currently used color.

    # Render helpers ----------------------------------------------------------
    def create_windows() -> None:
        """Create two windows and render the buttons inside."""
        ctx.win.append(
            ctx.m.mlx_new_window(
                ctx.p,
                ctx.scale * ctx.maze.width,
                ctx.scale * ctx.maze.height,
                "A-Maze-ing"))
        ctx.win.append(
            ctx.m.mlx_new_window(
                ctx.p,
                256,
                512,
                "Controls"))
        ctx.m.mlx_clear_window(ctx.p, ctx.win[0])
        ctx.m.mlx_clear_window(ctx.p, ctx.win[1])

        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win[1], ctx.gfx["button/regenerate"], 0, 0)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win[1], ctx.gfx["button/color"], 0, 128)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win[1], ctx.gfx["button/path"], 0, 256)
        ctx.m.mlx_put_image_to_window(
            ctx.p, ctx.win[1], ctx.gfx["button/exit"], 0, 384)
        ctx.m.mlx_do_sync(ctx.p)

    def render_maze_cells(subdir: str) -> None:
        """Render the backgrounds for the cells, the cells themselves,
        and the entry and exit."""
        ctx.m.mlx_do_sync(ctx.p)  # Reduces chance of corruption.
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                # Draw a colored background for the cell.
                ctx.m.mlx_put_image_to_window(
                    ctx.p, ctx.win[0],
                    ctx.gfx[f"{subdir}color/{colors[color_i]}"],
                    x * ctx.scale,
                    y * ctx.scale)

                # Draw the cell itself.
                walls = cell.get_walls()
                ctx.m.mlx_put_image_to_window(
                    ctx.p,
                    ctx.win[0],
                    ctx.gfx[f"{subdir}{walls:04b}"],
                    x * ctx.scale,
                    y * ctx.scale)

        x, y = maze.entry[0] * ctx.scale, maze.entry[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win[0],
            ctx.gfx[f"{subdir}obj/entry"], x, y)

        x, y = maze.exit[0] * ctx.scale, maze.exit[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win[0],
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
                ctx.win[0],
                ctx.gfx[f"{subdir}path"],
                x * ctx.scale,
                y * ctx.scale)
            ctx.m.mlx_do_sync(ctx.p)

    # Hooks -------------------------------------------------------------------
    def on_mouse(button: int, x: int, y: int, params: Any) -> None:
        nonlocal regenerate, color_i, path_visible
        if y < 127:  # Regenerate button.
            regenerate = True
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[0])
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[1])
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

        elif y > 384:  # Exit button.
            ctx.m.mlx_loop_exit(ctx.p)

    def on_key(keynum: int, params: Any) -> None:
        if keynum == 65307:
            ctx.m.mlx_loop_exit(ctx.p)

    def on_close(dummy: Any) -> None:
        ctx.m.mlx_loop_exit(ctx.p)

    # Environment and initial render ------------------------------------------
    create_windows()
    render_maze_cells(f"tile{ctx.scale}/")
    ctx.m.mlx_do_sync(ctx.p)

    # Setting up hooks --------------------------------------------------------
    ctx.m.mlx_mouse_hook(ctx.win[1], on_mouse, None)
    ctx.m.mlx_key_hook(ctx.win[0], on_key, None)
    ctx.m.mlx_key_hook(ctx.win[1], on_key, None)
    ctx.m.mlx_hook(ctx.win[0], 33, 0, on_close, None)

    ctx.m.mlx_loop(ctx.p)
    return regenerate
