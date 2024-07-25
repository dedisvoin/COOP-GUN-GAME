from copy import copy
import pygame

class Mouse:
    class Button:
        BTN_LEFT =              'LEFT'
        BTN_RIGHT =             'RIGHT'
        BTN_MIDDLE =            'MIDDLE'

    def __init__(self) -> None:
        self.__end_pos = [0, 0]
        self.__speed = [0, 0]
        self.__pressed = False
        self.__clicked = False

    @property
    def pos(self):
        return [*pygame.mouse.get_pos()]
    
    @property
    def speed(self):
        self.__speed = [
            self.pos[0]-self.__end_pos[0],
            self.pos[1]-self.__end_pos[1],
        ]
        self.__end_pos = copy(self.pos)
        return self.__speed
    
    def btn_convert(self, _btn: str) -> int:
        key = {
            'LEFT':     0,
            'MIDDLE':   1,
            'RIGHT':    2
        }
        return key[_btn]
    
    def press(self, _btn: str) -> bool:
        return pygame.mouse.get_pressed(3)[
            self.btn_convert(_btn)
        ]
    
    def click(self, _btn: str) -> bool:
        if not self.__pressed:
            if self.press(_btn):
                self.__pressed = True
                self.__clicked = True
        else:
            self.__clicked = False

        if not self.press(_btn):
            self.__pressed = False
            self.__clicked = False
        
        return self.__clicked

mouse_: Mouse = Mouse()
