import keyboard
import pygame
pygame.init()

class Keyboard:
    def __init__(self) -> 'Keyboard':
        self.__pressed = False
        self.__clicked = False

    def press(self, _key: str) -> bool:
        if pygame.mouse.get_focused():
            return keyboard.is_pressed(_key)
    
    def click(self, _key: str) -> bool:
        if not self.__pressed:
            if self.press(_key):
                self.__pressed = True
                self.__clicked = True
        else:
            self.__clicked = False

        if not self.press(_key):
            self.__pressed = False
            self.__clicked = False
        
        return self.__clicked

class Key:
    def __init__(self, key: str) -> None:
        self.__key = key
    
    @property
    def get(self): return self.__key


keyboard_ = Keyboard()