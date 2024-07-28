import pygame
import pygame.font


pygame.init()

fonts = []

def load_font(id: str | int, font_name: str, font_size: int, bold: bool = False, italic: bool = False):
    global fonts
    fonts.append([id,
        pygame.font.SysFont(font_name, font_size, bold, italic)
    ])

def load_font_by_file(id: str | int, file_name: str, font_size: int, bold: bool = False, italic: bool = False):
    global fonts
    __f = pygame.font.Font(file_name, font_size)
    __f.italic = italic
    __f.bold = bold
    fonts.append([
        id, __f
    ])

def get_font(id: str | int) -> pygame.font.Font:
    for font in fonts:
        if font[0] == id:
            return font[1]
    raise f'Font {id} not found!'
    

def render_font(surf: pygame.Surface, font_id: str | int, text: any, color: str | tuple[int, int, int], pos: tuple[int, int]):
    font = get_font(font_id)
    rendered_font = font.render(str(text), True, color)
    surf.blit(rendered_font, pos)

load_font('FPS_FONT', 'arial', 14, True, False)