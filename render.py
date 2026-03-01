import os
from typing import Any

from mlx import Mlx
import audio

from maze import Maze


class RenderError(Exception):
    pass


class Image:
    """Structure for image data"""
    def __init__(self):
        self.img = None
        self.width = 0
        self.height = 0
        self.data = None
        self.sl = 0  # size line
        self.bpp = 0  # bits per pixel
        self.iformat = 0


class Context:
    def __init__(self, maze: Maze):
        self.m = Mlx()  # The MLX class itself
        self.p = self.m.mlx_init()  # Pointer to the MLX connection
        self.gfx: dict[str, Image] = {}  # gfx means graphics
        self.win: list[Any] = []  # All our created windows
        self.maze = maze
        self.scale = 64  # Size of a tile (could be 32 or 64 pixels)


def get_png(ctx: Context, file: str) -> Image:
    """Returns a PNG image loaded from a filename."""
    img = Image()

    result = ctx.m.mlx_png_file_to_image(ctx.p, file)
    if not result:
        raise RenderError(f"failed loading PNG from {file}")
    img.img, img.width, img.height = result
    if not img.img:
        raise RenderError(f"failed creating image from {file}")

    # Get address
    img.data, img.bpp, img.sl, img.iformat = \
        ctx.m.mlx_get_data_addr(img.img)

    return img


def load_assets(ctx: Context, dir: str) -> None:
    """Load all assets from a directory, including its subdirectories."""
    for x in os.listdir(dir):
        file = f"{dir}/{x}"
        if os.path.isdir(file):
            load_assets(ctx, file)
        else:
            name = file.removeprefix("assets/").removesuffix(".png")
            ctx.gfx.update({name: get_png(ctx, file)})


def render(maze: Maze, path: list[str]) -> None:
    ctx = Context(maze)
    regenerate = False  # Whether to regenerate the maze after ending the loop
    path_visible = False

    # Setting correct scale ---------------------------------------------------
    w, h = ctx.m.mlx_get_screen_size(ctx.p)[1:]
    mw, mh = maze.width * ctx.scale, maze.height * ctx.scale
    # print("Maze size:", mw, mh)
    # print("Screen size:", w, h)
    if mw > w or mh > h:
        ctx.scale = 32

    # Colors ------------------------------------------------------------------
    colors = ["red", "green", "blue", "cyan", "pink", "yellow"]
    color_i = 0  # Index of the currently used color

    # Render helpers ----------------------------------------------------------
    def create_windows() -> None:
        ctx.win.append(ctx.m.mlx_new_window(ctx.p,
                                            ctx.scale * ctx.maze.width,
                                            ctx.scale * ctx.maze.height,
                                            "A-Maze-ing"))
        ctx.win.append(ctx.m.mlx_new_window(ctx.p, 256, 512, "Controls"))
        ctx.m.mlx_clear_window(ctx.p, ctx.win[0])
        ctx.m.mlx_clear_window(ctx.p, ctx.win[1])

    def render_maze_cells(subdir: str) -> None:
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                # Draw a colored background for the cell
                ctx.m.mlx_put_image_to_window(
                    ctx.p, ctx.win[0],
                    ctx.gfx[f"{subdir}color/{colors[color_i]}"].img,
                    x * ctx.scale,
                    y * ctx.scale)

                # Draw the cell itself
                walls = int(cell.to_hex(), 16)
                ctx.m.mlx_put_image_to_window(
                    ctx.p,
                    ctx.win[0],
                    ctx.gfx[f"{subdir}{walls:04b}"].img,
                    x * ctx.scale,
                    y * ctx.scale)

        x, y = maze.entry[0] * ctx.scale, maze.entry[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win[0],
            ctx.gfx[f"{subdir}obj/entry"].img, x, y)

        x, y = maze.exit[0] * ctx.scale, maze.exit[1] * ctx.scale
        ctx.m.mlx_put_image_to_window(
            ctx.p,
            ctx.win[0],
            ctx.gfx[f"{subdir}obj/exit"].img, x, y)

    def render_path(subdir: str) -> None:
        x, y = maze.entry
        for char in path:
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
            if (x, y) == maze.exit:
                audio.stop_music()
                break
            ctx.m.mlx_put_image_to_window(
                ctx.p,
                ctx.win[0],
                ctx.gfx[f"{subdir}path"].img,
                x * ctx.scale,
                y * ctx.scale)
            # ctx.m.mlx_do_sync(ctx.p)
            # time.sleep(0.05)

    # Hooks -------------------------------------------------------------------
    def on_mouse(button, x, y, params) -> None:
        nonlocal regenerate, color_i, path_visible
        if y < 127:  # Regnerate button
            regenerate = True
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[0])
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[1])
            ctx.m.mlx_loop_exit(ctx.p)

        elif 127 < y < 255:  # Color button
            color_i = (color_i + 1) % len(colors)
            render_maze_cells(f"tile{ctx.scale}/")
            if path_visible:
                render_path(f"tile{ctx.scale}/obj/")
            ctx.m.mlx_do_sync(ctx.p)

        elif 255 < y < 384:  # Path button
            if path_visible:
                render_maze_cells(f"tile{ctx.scale}/")
                path_visible = False
            else:
                render_path(f"tile{ctx.scale}/obj/")
                path_visible = True
            ctx.m.mlx_do_sync(ctx.p)

        elif y > 384:  # Exit button
            ctx.m.mlx_loop_exit(ctx.p)

    def on_key(keynum, params) -> None:
        if keynum == 65307:
            ctx.m.mlx_loop_exit(ctx.p)

    def on_close(dummy) -> None:
        ctx.m.mlx_loop_exit(ctx.p)

    # Environment and initial render ------------------------------------------
    load_assets(ctx, "assets")
    create_windows()
    render_maze_cells(f"tile{ctx.scale}/")
    ctx.m.mlx_do_sync(ctx.p)

    # Render second window buttons --------------------------------------------
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  ctx.gfx["button/regenerate"].img, 0, 0)
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  ctx.gfx["button/color"].img, 0, 128)
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  ctx.gfx["button/path"].img, 0, 256)
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  ctx.gfx["button/exit"].img, 0, 384)
    ctx.m.mlx_do_sync(ctx.p)

    # Setting up hooks --------------------------------------------------------
    ctx.m.mlx_mouse_hook(ctx.win[1], on_mouse, None)
    ctx.m.mlx_key_hook(ctx.win[0], on_key, None)
    ctx.m.mlx_key_hook(ctx.win[1], on_key, None)
    ctx.m.mlx_hook(ctx.win[0], 33, 0, on_close, None)

    ctx.m.mlx_loop(ctx.p)
    return regenerate
