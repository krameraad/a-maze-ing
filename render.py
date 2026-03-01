import os
# import random
from typing import Any
from mlx import Mlx
import audio

from maze import Maze


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
    def __init__(self, maze: Maze, tilesize: int):
        self.m = Mlx()  # The MLX class itself
        self.p = self.m.mlx_init()  # Pointer to the MLX connection
        self.gfx: dict[str, Image] = {}  # gfx means graphics
        self.win: list[Any] = []  # All our created windows
        self.maze = maze
        self.tilesize = tilesize


def load_image(mlx: Mlx, mlx_ptr: Any, file: str) -> Image:
    """Returns a PNG image loaded from a filename."""
    img = Image()

    result = mlx.mlx_png_file_to_image(mlx_ptr, file)
    if not result:
        raise Exception("failed to load PNG")
    img.img, img.width, img.height = result
    if not img.img:
        raise Exception("failed to create PNG")

    # Get address
    img.data, img.bpp, img.sl, img.iformat = \
        mlx.mlx_get_data_addr(img.img)

    return img


def create_windows(ctx: Context) -> None:
    ctx.win.append(ctx.m.mlx_new_window(ctx.p,
                                        ctx.tilesize * ctx.maze.width,
                                        ctx.tilesize * ctx.maze.height,
                                        "A-Maze-ing"))
    ctx.win.append(ctx.m.mlx_new_window(ctx.p, 256, 384, "Controls"))
    for window in ctx.win:
        ctx.m.mlx_clear_window(ctx.p, window)


def render(maze: Maze, path: list[str]) -> None:
    ctx = Context(maze, 64)

    dir_assets = "./assets/"
    imgs: dict[str, Image] = {}
    colors = ["color_red", "color_green", "color_blue", "color_me"]
    color_index, color_len = 0, len(colors)

    regenerate = False

    # Render helpers ----------------------------------------------------------
    def render_background() -> None:
        for y in range(maze.height):
            for x in range(maze.width):
                ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[0],
                                              imgs[colors[color_index]].img,
                                              x * ctx.tilesize,
                                              y * ctx.tilesize)

    def render_maze_cells() -> None:
        for y, row in enumerate(maze.grid):
            for x, cell in enumerate(row):
                walls = int(cell.to_hex(), 16)
                ctx.m.mlx_put_image_to_window(ctx.p,
                                              ctx.win[0],
                                              imgs[f"tile_{walls:04b}"].img,
                                              x * ctx.tilesize,
                                              y * ctx.tilesize)
        ex, ey = maze.entry[0] * ctx.tilesize, maze.entry[1] * ctx.tilesize
        ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[0],
                                      imgs["tile_entry"].img, ex, ey)
        ex, ey = maze.exit[0] * ctx.tilesize, maze.exit[1] * ctx.tilesize
        ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[0],
                                      imgs["tile_exit"].img, ex, ey)

    def render_path() -> None:
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
            ctx.m.mlx_put_image_to_window(ctx.p,
                                          ctx.win[0],
                                          imgs["tile_path"].img,
                                          x * ctx.tilesize,
                                          y * ctx.tilesize)
            # ctx.m.mlx_do_sync(ctx.p)
            # time.sleep(0.1)

    # Hooks -------------------------------------------------------------------
    def on_mouse(button, x, y, params) -> None:
        nonlocal regenerate, color_index
        if y < 127:
            regenerate = True
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[0])
            ctx.m.mlx_destroy_window(ctx.p, ctx.win[1])
            ctx.m.mlx_loop_exit(ctx.p)
        elif 127 < y < 255:
            color_index = (color_index + 1) % color_len
            render_background()
            render_maze_cells()
            render_path()
            ctx.m.mlx_do_sync(ctx.p)
        elif y > 255:
            ctx.m.mlx_loop_exit(ctx.p)

    def on_key(keynum, params) -> None:
        if keynum == 65307:
            ctx.m.mlx_loop_exit(ctx.p)

    def on_close(dummy) -> None:
        ctx.m.mlx_loop_exit(ctx.p)

    create_windows(ctx)

    # Loading images ----------------------------------------------------------
    for x in os.listdir(dir_assets):
        imgs[x.removesuffix(".png")] = load_image(ctx.m, ctx.p, dir_assets + x)

    # Initial render ----------------------------------------------------------
    render_background()
    render_maze_cells()
    render_path()
    ctx.m.mlx_do_sync(ctx.p)

    # Render second window buttons --------------------------------------------
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  imgs["button_regenerate"].img, 0, 0)
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  imgs["button_color"].img, 0, 128)
    ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
                                  imgs["button_exit"].img, 0, 256)
    # ctx.m.mlx_put_image_to_window(ctx.p, ctx.win[1],
    #                               imgs["button_path"].img, 0, 384)
    ctx.m.mlx_do_sync(ctx.p)

    # Setting up hooks --------------------------------------------------------
    ctx.m.mlx_mouse_hook(ctx.win[1], on_mouse, None)
    ctx.m.mlx_key_hook(ctx.win[0], on_key, None)
    ctx.m.mlx_key_hook(ctx.win[1], on_key, None)
    ctx.m.mlx_hook(ctx.win[0], 33, 0, on_close, None)

    ctx.m.mlx_loop(ctx.p)
    return regenerate
