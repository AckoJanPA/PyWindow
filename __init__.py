import pygame
try:
    import PyWindow.icons as icons
except:
    import icons

def clamp(value, min_val, max_val):
    """Clamps a value between a minimum and a maximum."""
    return min(max(value, min_val), max_val)

pygame.init()

class WindowStyle:
    def __init__(self, border_color = (255, 255, 255), text_color = (0, 0, 0), close_button_path = icons.CLOSE_BLACK, title_bar_size = 16, round_corners = True, font_name = "Arial", use_ttf_file = False, title_bold = False, title_italic = False):
        """
        if `use_ttf_file` is `True`, instead of using a system font with the name of `font_name`,
        loads a file with the path of `font_name`
        """

        self.border = border_color
        self.text = text_color
        self.close_button = pygame.image.load(close_button_path)
        self.title_bar_size = title_bar_size
        self.font_name = font_name
        self.round_corners = round_corners
        self.use_ttf_file = use_ttf_file
        self.title_bold = title_bold
        self.title_italic = title_italic

class Window:
    CLOSE = 1
    DRAGGED = 2
    
    START_TOP_LEFT = "top-left"
    START_TOP_RIGHT = "top-right"
    START_BOTTOM_LEFT = "bottom-left"
    START_BOTTOM_RIGHT = "bottom-right"
    START_CENTER = "center"

    def __init__(self, parent: pygame.Surface, width: int, height: int, title: str = "Window", start_pos="top-left", window_style : WindowStyle = WindowStyle(), icon=None):
        self.surface = pygame.Surface((width, height))

        self.x = 0
        self.y = 0

        if isinstance(start_pos, tuple):
            self.x = start_pos[0]
            self.y = start_pos[1]

        else:
            match start_pos:
                case Window.START_TOP_LEFT:
                    self.x = 0
                    self.y = 0

                case Window.START_TOP_RIGHT:
                    self.x = parent.get_width() - (width + 10)
                    self.y = 0

                case Window.START_BOTTOM_LEFT:
                    self.x = 0
                    self.y = parent.get_height() - (height + 15 + window_style.title_bar_size)

                case Window.START_BOTTOM_RIGHT:
                    self.x = parent.get_width() - (width + 10)
                    self.y = parent.get_height() - (height + 15 + window_style.title_bar_size)

                case Window.START_CENTER:
                    self.x = (parent.get_width() / 2) - ((width + 10) / 2)
                    self.y = (parent.get_height() / 2) - ((height + 15 + window_style.title_bar_size) / 2)
        
        self.width = width
        self.height = height
        self.title = title
        self.round_corners = window_style.round_corners

        self.parent = parent

        self.font = None

        if window_style.use_ttf_file:
            self.font = pygame.font.Font(window_style.font_name, window_style.title_bar_size)
        else:
            self.font = pygame.font.SysFont(window_style.font_name, window_style.title_bar_size, window_style.title_bold, window_style.title_italic)

        self.close_button = pygame.Rect(self.width + 5 - 16, 5, 16, 16)
        self.grab_area = pygame.Rect(0, 0, self.width + 10, window_style.title_bar_size + 10)
        
        self.grab_offset = None

        self.close_func = lambda: Window.CLOSE
        self.tick_func = lambda self: None

        self.style = window_style

        self.icon = None

        self.hidden = False
        
        if icon:
            self.icon = pygame.image.load(icon)
    
    def fill(self, color):
        self.surface.fill(color)
    
    def blit(self, surface, coordinates):
        self.surface.blit(surface, coordinates)
    
    def render(self):
        if not self.hidden:
            text_size = self.font.get_height()

            finish = pygame.Surface((self.width + 10, self.height + 15 + text_size), pygame.SRCALPHA)

            pygame.draw.rect(
                finish,
                self.style.border,
                pygame.Rect(
                    0,
                    0,
                    finish.get_width(),
                    finish.get_height()
                ),
                border_radius = 5 if self.round_corners else 0
            )
            
            finish.blit(self.surface, (5, 10 + text_size))

            finish.blit(
                self.font.render(self.title, True, self.style.text),
                (5 + text_size + 5 if self.icon else 5, 5)
            )

            if self.icon:
                finish.blit(
                    pygame.transform.scale(self.icon, (text_size, text_size)),
                    (5, 5)
                )

            finish.blit(self.style.close_button, (self.width - 11, 5))

            self.parent.blit(finish, (self.x, self.y))
    
    def tick(self, can_be_moved = True) -> int:
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if not mouse_pressed:
            self.grab_offset = None

        moved_close_button = pygame.Rect(self.close_button.x + self.x, self.close_button.y + self.y, self.close_button.width, self.close_button.height)
        moved_grab_area = pygame.Rect(self.x, self.y, self.grab_area.width, self.grab_area.height)

        if mouse_pressed and moved_close_button.collidepoint(mouse_pos) and (not self.grab_offset):
            return self.close_func()
        
        
        elif ((mouse_pressed and moved_grab_area.collidepoint(mouse_pos)) or self.grab_offset) and can_be_moved:
            if not self.grab_offset:
                self.grab_offset = (
                    self.x - mouse_pos[0],
                    self.y - mouse_pos[1]
                )
            else:
                self.x = self.grab_offset[0] + mouse_pos[0]
                self.y = self.grab_offset[1] + mouse_pos[1]
            
            self.x = clamp(self.x, 0, self.parent.get_width() - self.width - 10)
            self.y = clamp(self.y, 0, self.parent.get_height() - self.height - self.font.get_height() - 15)
            
            return Window.DRAGGED
            
        self.x = clamp(self.x, 0, self.parent.get_width() - self.width - 10)
        self.y = clamp(self.y, 0, self.parent.get_height() - self.height - self.font.get_height() - 15)

        return self.tick_func(self)


class WindowContainer:
    def __init__(self, parent: pygame.Surface):
        self.children: list[Window] = []
        self.ordered: list[Window] = []
        self.parent = parent
        self.can_other_be_focused = True
        self.id_map = {}
    
    def render(self):
        for win in reversed(self.children):
            win.render()
    
    def tick(self):
        do_process = True

        if not pygame.mouse.get_pressed()[0]:
            self.can_other_be_focused = True

        for win_id, win in enumerate(self.children):
            if do_process and self.can_other_be_focused:
                match win.tick():
                    case Window.CLOSE:
                        self.ordered.pop(
                            self.ordered.index(
                                self.children.pop(win_id)
                            )
                        )

                        do_process = False
                        
                        self.can_other_be_focused = False

                    case Window.DRAGGED:
                        self.children.pop(win_id)
                        self.children.insert(0, win)
                        
                        do_process = False
            else:
                win.tick(False)
    
    def get_window(self, title) -> Window:
        for win in self.ordered:
            if title == win.title:
                return win
    
    def delete_window(self, title):
        win = self.get_window(title)

        if win:
            self.ordered.pop(
                self.ordered.index(
                    win
                )
            )
            self.children.pop(
                self.children.index(
                    win
                )
            )
    
    def add_window(self, width: int, height: int, title: str = "Window", start_pos=Window.START_TOP_LEFT, window_style: WindowStyle = WindowStyle(), icon=icons.PYWIN_ICON, id_in_map = None):
        window = Window(self.parent, width, height, title, start_pos, window_style, icon)

        self.children.insert(0, window)
        self.ordered.append(window)

        if id_in_map:
            self.id_map[id_in_map] = window
        else:
            self.id_map[len(self.id_map)] = window
    
    def connect_close_func(self, window_id: int, function: callable = lambda: Window.CLOSE):
        self.children[window_id].close_func = function


if __name__ == "__main__":
    print()
    for i, text in enumerate(
        [
            "WindowContainer"
        ]
    ):
        print(f"{i}. - {text}")

    preview = int(input("\nEnter preview id > ").strip())

    if preview == 0:
        root = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

        container = WindowContainer(root)

        container.add_window(150 * 2, 100 * 2, "pygame window", start_pos=Window.START_CENTER)

        just_opened = False

        win_id = 0

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
            
            root.fill((0, 0, 0))

            container.render()

            container.tick()

            pygame.display.flip()

            if (not just_opened) and pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                just_opened = True
                
                win_id += 1
                container.add_window(150 * 2, 100 * 2, f"New Window {win_id}",  start_pos=Window.START_CENTER)

            if not pygame.key.get_pressed()[pygame.K_KP_PLUS]:
                just_opened = False
