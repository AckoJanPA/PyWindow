import pygame

pygame.init()

class PyWindow:
    CLOSE = 1

    def __init__(self, width: int, height: int, x: int = 0, y: int = 0, title: str = "PyWindow", title_font_size = 24):
        self.surface = pygame.Surface((width, height))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title

        self.font = pygame.font.Font(None, title_font_size)

        self.fill(((50, 50, 50)))
    
    def fill(self, color):
        self.surface.fill(color)
    
    def blit(self, surface, coordinates):
        self.surface.blit(surface, coordinates)
    
    def render(self, destination):
        text_size = self.font.get_height()

        finish = pygame.Surface((self.width + 10, self.height + 15 + text_size))

        pygame.draw.rect(
            finish,
            (100, 100, 100),
            pygame.Rect(
                0,
                0,
                finish.get_width(),
                finish.get_height()
            ),
            border_radius=10
        )

        finish.blit(self.surface, (5, 10 + text_size))

        finish.blit(
            self.font.render(self.title, True, (255, 255, 255)),
            (5, 5)
        )

        destination.blit(finish, (self.x, self.y))
    
    def tick(self) -> int:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return PyWindow.CLOSE

if __name__ == "__main__":
    root = pygame.display.set_mode((800, 600))

    pywin = PyWindow(150 * 2, 100 * 2)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        
        root.fill((0, 0, 0))

        pywin.render(root)

        match pywin.tick():
            case PyWindow.CLOSE:
                pywin.fill("#ff0000")

        pygame.display.flip()
