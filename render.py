import sys
import os
from typing import Any

from mlx import Mlx

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


# class Context:
#     def __init__(self):
#         self.imgs: dict[str, Image] = {}


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


def render(maze: Maze, path: list[str]) -> None:
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    # ctx = Context()

    dir_assets = "./assets/"
    imgs: dict[str, Image] = {}

    tilesize = 64
    w: int = tilesize * maze.width
    h: int = tilesize * maze.height

    # Hooks -------------------------------------------------------------------
    def mymouse(button, x, y, params):
        print(f"Got mouse event! button {button} at {x},{y}.")

    def mykey(keynum, params):
        if keynum == 65307:
            mlx.mlx_loop_exit(mlx_ptr)

    def gere_close(dummy):
        mlx.mlx_loop_exit(mlx_ptr)

    # Creating a window -------------------------------------------------------
    win_1 = mlx.mlx_new_window(mlx_ptr, w, h, "A-Maze-ing")
    mlx.mlx_clear_window(mlx_ptr, win_1)

    # Loading images ----------------------------------------------------------
    for x in os.listdir(dir_assets):
        imgs[x.removesuffix(".png")] = load_image(mlx, mlx_ptr, dir_assets + x)

    # Render the maze cells
    for y, row in enumerate(maze.grid):
        for x, cell in enumerate(row):
            walls = int(cell.to_hex(), 16)
            mlx.mlx_put_image_to_window(mlx_ptr,
                                        win_1,
                                        imgs[f"tile_{walls:04b}"].img,
                                        x * tilesize,
                                        y * tilesize)

    # Render path
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
            break
        mlx.mlx_put_image_to_window(mlx_ptr,
                                    win_1,
                                    imgs["tile_path"].img,
                                    x * tilesize,
                                    y * tilesize)

    # Render entry and exit
    x, y = maze.entry[0] * tilesize, maze.entry[1] * tilesize
    mlx.mlx_put_image_to_window(mlx_ptr, win_1, imgs["tile_entry"].img, x, y)
    x, y = maze.exit[0] * tilesize, maze.exit[1] * tilesize
    mlx.mlx_put_image_to_window(mlx_ptr, win_1, imgs["tile_exit"].img, x, y)

    # Setting up hooks --------------------------------------------------------
    mlx.mlx_mouse_hook(win_1, mymouse, None)
    mlx.mlx_key_hook(win_1, mykey, None)
    mlx.mlx_hook(win_1, 33, 0, gere_close, None)

    mlx.mlx_loop(mlx_ptr)
    