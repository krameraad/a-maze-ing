import os
import pygame

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"


def init_audio() -> None:
    if not pygame.get_init():
        pygame.init()


def play_music(path: str, loop: bool = True) -> None:
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1 if loop else 0)


def stop_music() -> None:
    pygame.mixer.music.stop()


def play_sound(path: str) -> None:
    sound = pygame.mixer.Sound(path)
    sound.play()
