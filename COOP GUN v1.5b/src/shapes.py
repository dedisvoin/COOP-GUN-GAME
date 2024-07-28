from pygame import gfxdraw

from src.constants import *
from src.functs import Vec2

import pygame

class shapes:
    class Circle:
        def __init__(self, 
                pos: list, 
                radius: int, 
                color: tuple[int, int, int] = STANDART_SHAPES_FILL_COLOR,
                outline_width: int = STANDART_SHAPES_OUTLINE_WIDTH,
                outline_color: tuple[int, int, int] = STANDART_SHAPES_OUTLINE_COLOR
            ) -> 'shapes.Circle':
            self.__pos = pos
            self.__radius = radius
            self.__color = color
            self.__outline_color = outline_color
            self.__outline_width = outline_width

        @property
        def pos(self) -> list:
            return self.__pos
        
        @pos.setter
        def pos(self, _pos: list[int, int]):
             self.__pos = _pos

        @property
        def radius(self) -> int:
             return self.__radius
        
        @radius.setter
        def radius(self, _radius: int):
             self.__radius = _radius

        def __del__(self):
             del self

        def __str__(self):
             return f'Circle: pos={self.__pos}, radius={self.__radius}, color={self.__color}, outline_color={self.__outline_color}, outline_width={self.__outline_width}'

        def draw(self, surf: pygame.Surface) -> None:
            pygame.draw.circle(surf, self.__color, self.__pos, self.__radius)
            if self.__outline_width > 0:
                pygame.draw.circle(surf, self.__outline_color, self.__pos, self.__radius, self.__outline_width)


    @classmethod
    def circle(self, 
            surf: pygame.Surface,
            pos: list, 
            radius: int,
            color: tuple[int, int, int] = STANDART_SHAPES_FILL_COLOR,
            outline_width: int = STANDART_SHAPES_OUTLINE_WIDTH,
            outline_color: tuple[int, int, int] = STANDART_SHAPES_OUTLINE_COLOR,
            width: int = 0
        ) -> None:
        pygame.draw.circle(surf, color, pos, radius, width)
        if outline_width > 0:
            pygame.draw.circle(surf, outline_color, pos, radius, outline_width)


    @classmethod
    def __radius__(self, radius: int | float | tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        if (type(radius) == int) or (type(radius) == float):
            return [radius, radius, radius, radius]
        elif type(radius) is list:
            return radius


    class Rect:
        def __init__(self,
                pos: list[int],
                size: list[int],
                color: tuple[int, int, int] = STANDART_SHAPES_FILL_COLOR,
                radius: int | float | tuple[int, int, int, int] = STANDART_SHAPES_RECT_RADIUS,
                outline_width: int = STANDART_SHAPES_OUTLINE_WIDTH,
                outline_color: tuple[int, int, int] = STANDART_SHAPES_OUTLINE_COLOR
        ) -> 'shapes.Rect':
            self.__pos = pos
            self.__size = size
            self.__color = color
            self.__radius = radius
            self.__outline_color = outline_color
            self.__outline_width = outline_width

        @property
        def pos(self) -> list:
            return self.__pos
        
        @pos.setter
        def pos(self, _pos: list[int, int]):
            self.__pos = _pos

        @property
        def height(self) -> int:
            return self.__size[1]

        @property
        def width(self) -> int:
            return self.__size[0]
        
        @height.setter
        def height(self, _height: int):
            self.__size[1] = _height

        @width.setter
        def width(self, _width: int):
            self.__size[0] = _width

        def draw(self, surf: pygame.Surface) -> None:
            pygame.draw.rect(surf, self.__color, [self.__pos, self.__size], 0, *self.__radius__(self.__radius))
            if self.__outline_width>0:
                pygame.draw.rect(surf, self.__outline_color, [self.__pos, self.__size], self.__outline_width, *self.__radius__(self.__radius))


    @classmethod
    def rect(self,
            surf: pygame.Surface,
            pos: list[int],
            size: list[int],
            color: tuple[int, int, int] = STANDART_SHAPES_FILL_COLOR,
            radius: int | float | tuple[int, int, int, int] = STANDART_SHAPES_RECT_RADIUS,
            width: int = STANDART_SHAPE_WIDTH,
            outline_width: int = STANDART_SHAPES_OUTLINE_WIDTH,
            outline_color: tuple[int, int, int] = STANDART_SHAPES_OUTLINE_COLOR
        ) -> None:
        pygame.draw.rect(surf, color, [pos, size], width, *self.__radius__(radius))
        if outline_width > 0:
            pygame.draw.rect(surf, outline_color, [pos, size], outline_width, *self.__radius__(radius))

    @classmethod
    def line(self,
             surf: pygame.Surface,
             pos1: list[int],
             pos2: list[int],
             size: int = STANDART_LINE_SIZE,
             color: tuple[int, int, int] = STANDART_LINE_COLOR,
             fast: bool = True,
             circled: bool = False
             ):
        if circled:
            self.circle(surf, pos1, size / 2 + 0.5, color)
            self.circle(surf, pos2, size / 2 + 0.5, color)
        if fast:
            pygame.draw.line(surf, color, pos1, pos2, size)
        else:
            poligone_points = []

            vec_normal = Vec2.two_points(pos2, pos1)
            
            vec_rotated_90 = vec_normal.copy()
            vec_rotated_90.rotate(180 - vec_normal.angle + 45)
            vec_rotated_90.normalize_at()
            
            vec_rotated_90 *= size / 2
            
            poligone_points = [
                [pos1[0] + vec_rotated_90.x, pos1[1] + vec_rotated_90.y],
                [pos1[0] - vec_rotated_90.x, pos1[1] - vec_rotated_90.y],
                [pos2[0] - vec_rotated_90.x, pos2[1] - vec_rotated_90.y],
                [pos2[0] + vec_rotated_90.x, pos2[1] + vec_rotated_90.y]
            ]

            if vec_rotated_90.is_dot:
                if pos1[1] > pos2[1]:   
                    self.rect(surf, [pos2[0]-size/2, pos2[1]], [size, pos1[1]-pos2[1]], color)
                elif pos1[1] < pos2[1]:
                    self.rect(surf, [pos1[0]-size/2, pos1[1]], [size, pos2[1]-pos1[1]], color)
            else:
                self.polygon(surf, poligone_points, color)


    @classmethod
    def lines(self,
             surf: pygame.Surface,
             points: list[dict[int, int]],
             size: int = STANDART_LINE_SIZE,
             color: tuple[int, int, int] = STANDART_LINE_COLOR,
             fast: bool = True,
             circled: bool = False
             ):
        for i in range(0, len(points) - 1):
            self.line(surf, points[i], points[i + 1], size, color, fast, circled)
            

    @classmethod
    def polygon(self,
                surf: pygame.Surface,
                points: list[dict[int, int]],
                color: tuple[int, int, int] = STANDART_SHAPES_FILL_COLOR,
                width: int = 0
            ):
        pygame.draw.polygon(surf, color, points, width)

    class fast:
        @classmethod
        def v_line(self,
                   surf: pygame.Surface,
                   x: int,
                   y1: int,
                   y2: int,
                   color: tuple[int, int, int] = STANDART_LINE_COLOR,
                   size: int = STANDART_LINE_SIZE
                ):
            
            for i in range(0, size):
                gfxdraw.vline(surf, int(x) - size // 2 + i, int(y1), int(y2), color)


        @classmethod
        def h_line(self,
                   surf: pygame.Surface,
                   y: int,
                   x1: int,
                   x2: int,
                   color: tuple[int, int, int] = STANDART_LINE_COLOR,
                   size: int = STANDART_LINE_SIZE
                ):
            
            for i in range(0, size):
                gfxdraw.hline(surf, int(x1), int(x2), int(y) - size // 2 + i, color)