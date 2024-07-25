import pygame_shaders
import pygame


def shaders_clear(color: tuple[int, int, int]):
    pygame_shaders.clear(color)



class Shader:
    def __init__(self, vertex_path: str, fragment_path: str, size: tuple[int, int], pos: tuple[int, int] = [0, 0]) -> None:
        self.__vertex_path = vertex_path
        self.__fragment_path = fragment_path
        self.__size = size
        self.__pos = pos
        self.__shader = pygame_shaders.Shader(size=self.__size, display=self.__size, 
                        pos=self.__pos, vertex_path=self.__vertex_path, 
                        fragment_path=self.__fragment_path)
        
    def render(self, surf: pygame.Surface, color: tuple[int, int, int] = [0, 0, 0]):
        shaders_clear(color)
        self.__shader.render(surf)

    def send(self, value_name: str, data):
        self.__shader.send(value_name, data)

