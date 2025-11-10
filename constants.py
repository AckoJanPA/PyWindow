try:
    import PyWindow as lib
except:
    import __init__ as lib
import pygame
try:
    import PyWindow.icons as icons
except:
    import icons

class WindowStyles:
    LIGHT_MODE_ROUND = lib.WindowStyle()
    DARK_MODE_ROUND = lib.WindowStyle(
        (50, 50, 50),
        (255, 255, 255),
        icons.CLOSE_WHITE,
        16,
        True,
        "Arial",
        False,
        False,
        False
    )
    LIGHT_MODE_SQUARE = lib.WindowStyle(round_corners=False)
    DARK_MODE_SQUARE = lib.WindowStyle(
        (50, 50, 50),
        (255, 255, 255),
        icons.CLOSE_WHITE,
        16,
        False,
        "Arial",
        False,
        False,
        False
    )
    MINIMAL_DARK_MODE = lib.WindowStyle(
        (30, 30, 30),
        (200, 200, 200),
        icons.CLOSE_WHITE,
        12,
        False,
        "Consolas",
        True
    )

if __name__ == '__main__':
    root = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

    container = lib.WindowContainer(root)

    container.add_window(200, 175, "light mode round", lib.Window.START_TOP_LEFT, WindowStyles.LIGHT_MODE_ROUND)
    container.add_window(200, 175, "dark mode round", lib.Window.START_TOP_LEFT, WindowStyles.DARK_MODE_ROUND)
    container.add_window(200, 175, "light mode square", lib.Window.START_TOP_LEFT, WindowStyles.LIGHT_MODE_SQUARE)
    container.add_window(200, 175, "dark mode square", lib.Window.START_TOP_LEFT, WindowStyles.DARK_MODE_SQUARE)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        
        root.fill((0, 0, 0))

        container.render()

        container.tick()

        pygame.display.flip()
