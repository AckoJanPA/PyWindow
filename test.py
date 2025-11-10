import pygame
import __init__ as lib
from constants import WindowStyles

root = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

container = lib.WindowContainer(root)

container.add_window(150, 100, "Hello World!", (10, 10), window_style=WindowStyles.LIGHT_MODE_SQUARE, icon=lib.icons.PYTHON)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

    root.fill((0, 0, 0))

    container.render()

    container.tick()

    pygame.display.flip()
