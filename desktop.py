try:
    from PyWindow import Window, WindowContainer, pygame
except:
    from __init__ import Window, WindowContainer, pygame

class Desktop:
    def __init__(self, parent, bg_color = "#81baff", hotbar_color = "#abcffb"):
        self.parent = parent

        self.surface = pygame.Surface(
            (
                parent.get_width(),
                parent.get_height() - 42,
            )
        )

        self.bg_color = bg_color
        self.hotbar_color = hotbar_color

        self.win_container: WindowContainer = WindowContainer(self.surface)
    
    def update(self):
        self.win_container.tick()

        self.parent.fill(self.hotbar_color)

        self.surface.fill(self.bg_color)
        self.win_container.render()

        self.parent.blit(self.surface, (0, 0))

        y = self.parent.get_height() - 42 + 5

        for idx, app_open in enumerate(self.win_container.ordered):
            x = idx * 32 + 5

            self.parent.blit(pygame.transform.scale(app_open.icon, (32, 32)), (x, y))
