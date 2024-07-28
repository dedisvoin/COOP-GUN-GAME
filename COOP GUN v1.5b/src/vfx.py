from random import randint
from src.functs import *

class Color:
    def __init__(self) -> None:
        self.__r = 0
        self.__g = 0
        self.__b = 0
        self.__a = 1

    def __str__(self) -> str:
        return f'{self.__r}, {self.__g}, {self.__b}, {self.__a}'

    @property
    def r(self): return self.__r

    @property
    def g(self): return self.__g

    @property
    def b(self): return self.__b

    @r.setter
    def r(self, r: int):
        self.__r = r

    @g.setter
    def g(self, g: int):
        self.__g = g

    @b.setter
    def b(self, b: int):
        self.__b = b

    def get(self):
        return [self.__r, self.__g, self.__b]

    def rgb(self, r: int, g: int, b: int) -> 'Color':
        self.__r = r
        self.__g = g
        self.__b = b
        return self
    
    def hex(self, hex: str) -> 'Color':
        if hex.startswith('#'):
            hex = hex[1:]
        if len(hex) == 3:
            self.__r = int(hex[0], 16)
            self.__g = int(hex[1], 16)
            self.__b = int(hex[2], 16)
        elif len(hex) == 6:
            self.__r = int(hex[0:2], 16)
            self.__g = int(hex[2:4], 16)
            self.__b = int(hex[4:6], 16)
        elif len(hex) == 8:
            self.__r = int(hex[0:2], 16)
            self.__g = int(hex[2:4], 16)
            self.__b = int(hex[4:6], 16)
            self.__a = int(hex[6:8], 16)
        else:
            raise ValueError('Invalid hex color')
        return self
    
    @classmethod
    def random(self) -> 'Color':
        color = Color()
        color.r = randint(0, 255)
        color.g = randint(0, 255)
        color.b = randint(0, 255)
        return color
    
class ParticleTypes:
    FILLED_CIRCLE = 'filled_circle'
    FILLED_RECT = 'filled_rect'

class Particle:
    def __init__(self, pos: Vec2, speed: Vec2, type: ParticleTypes) -> None:
        self.pos = pos
        self.type = type
        self.speed = speed