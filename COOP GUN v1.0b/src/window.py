
import os
import keyboard
import pygame
from src.constants import *
from src.text import *

class WindowFlags:
    FULLSCREEN =                   pygame.FULLSCREEN
    RESIZE =                       pygame.RESIZABLE
    SCALE =                        pygame.SCALED
    NO_FRAME =                     pygame.NOFRAME
    OPENGL =                       pygame.OPENGL

class WindowEvents:
    def __init__(self) -> 'WindowEvents':
        self.__whell = 0
        self.__window_resized = False

    def update(self):
        self.__whell = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                os._exit(-1)
            if event.type == pygame.MOUSEWHEEL:
                self.__whell = event.y
            if event.type == pygame.WINDOWRESIZED:
                self.__window_resized = True
    
    @property
    def whell(self):
        return self.__whell
    
    @property
    def resized(self):
        return self.__window_resized

class Window:
    def __init__(self, 
                 _size: list[int] = STANDART_WINDOW_SIZE, 
                 _title: str = STANDART_WINDOW_TITLE, 
                 _events: WindowEvents = WindowEvents(),
                 _vsync: bool = STANDART_WINDOW_VSYNC, 
                 _flags: WindowFlags = WindowFlags.RESIZE,
                 _pos: list = [0, 0],
                 _render_fps: bool = True
                 ) -> 'Window':
                 
        self.__title = _title
        self.__size = _size
        self.__flags = _flags
        self.__vsync = _vsync
        self.__events = _events
        self.__exit_key = 'esc'
        self.__opened = True
        self.__window = pygame.display.set_mode(_size, _flags, 0, 0, _vsync)
        
        self.__timer = pygame.time.Clock()
        self.fps = 60
        self.__pos = _pos
        self.__rendered_fps = _render_fps
        
        pygame.display.set_caption(_title)  

    def set_exit_key(self, key):
        self.__exit_key = key

    def __render_fps(self):
        if 120 <= self.get_fps:
            _fps_color = 'black'
        if 60 <= self.get_fps < 120:
            _fps_color = 'green'
        if 30 <= self.get_fps < 60:
            _fps_color = 'orange'
        if self.get_fps < 30:
            _fps_color = 'red'
        render_font(self.__window, 'FPS_FONT', f'fps: {self.get_fps}', _fps_color, [5, 5])


    def render_fps(self):
        if self.__rendered_fps: self.__render_fps()
        
        
    def update(self, _bg_color: tuple[int, int, int] = STANDART_WINDOW_BG_COLOR):
        self.fps = max(0, self.fps)
        self.__timer.tick(self.fps)
        self.__events.update()
        
        
        self.__size = [*pygame.display.get_window_size()]
        
        if keyboard.is_pressed(self.__exit_key):
            self.__opened = False
            pygame.quit()
            os._exit(-1)
            return False
        
        pygame.display.flip()
        self.__window.fill(_bg_color)

        

        return self.__opened
    

        
    def get_delta(self, target_fps: float | int) -> float:
        return target_fps / (self.get_fps+0.000001)
    
    @property
    def surf(self):
        return self.__window
    
    @property
    def surf_size(self) -> list[int]:
        return [*self.surf.get_size()]
    
    @property
    def size(self) -> list[int]:
        return self.__size
    
    @property
    def vsync(self) -> bool:
        return self.__vsync
    
    @property
    def get_fps(self) -> float:
        return int(self.__timer.get_fps())
    
    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def center(self) -> list[int]:
        return [
            self.size[0] / 2,
            self.size[1] / 2
        ]
    
    @title.setter
    def title(self, _title: str):
        pygame.display.set_caption(_title)
        self.__title = _title

    @property
    def flags(self) -> WindowFlags:
        return self.__flags
    
    @property
    def whell(self):
        return self.__events.whell
    
    