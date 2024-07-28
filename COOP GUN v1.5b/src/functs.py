from copy import copy

import pygame
from src.constants import LARGE_NUMBER
import random
import math






class Vec2:
    @classmethod
    def two_points(self, point1: tuple[int | float, int | float], point2: tuple[int | float, int | float]) -> 'Vec2':
        return Vec2(point1[0] - point2[0], point1[1] - point2[1])
    
    @classmethod
    def random(self):
        return Vec2(random.randint(-LARGE_NUMBER, LARGE_NUMBER), 
                    random.randint(-LARGE_NUMBER, LARGE_NUMBER)).normalize()

    def __init__(self, x: int | float = 0, y: int | float = 0) -> None:
        self._x = x
        self._y = y

    def copy(self):
        return Vec2(copy(self._x), copy(self._x))

    def __add__(self, vec2):
        return Vec2(self._x + vec2.x, self._y + vec2.y)
    
    def __sub__(self, vec2):
        return Vec2(self._x - vec2.x, self._y - vec2.y)
    
    def __iadd__(self, vec2):
        return Vec2(self._x + vec2.x, self._y + vec2.y)
    
    def __isub__(self, vec2):
        return Vec2(self._x - vec2.x, self._y - vec2.y)
    
    def __mul__(self, value):
        return Vec2(self._x * value, self._y * value)
    
    def __itruediv__(self, value):
        return Vec2(self._x / value, self._y / value)

    def __len__(self):
        return self.lenght()
    
    def __str__(self):
        return f'Vector <{self._x, self._y}>'
    
    @property
    def x(self): return self._x

    @property
    def y(self): return self._y

    @property
    def xy(self): return [self._x, self._y]

    @x.setter
    def x(self, x: int | float):
        self._x = x

    @y.setter
    def y(self, y: int | float):
        self._y = y

    def lenght(self):
        return math.sqrt(self._x ** 2 + self._y ** 2) + 0.0001
    
    def normalize_at(self):
        l = self.lenght()
        self._x /= l
        self._y /= l

    def normalize(self) -> 'Vec2':
        l = self.lenght()
        return Vec2(self._x / l, self._y / l)
    
    @property
    def angle(self):
        return abs(math.degrees((math.atan2(self._y, self._x) - math.pi)))
    
    @angle.setter
    def angle(self, a):
        ang = self.angle - a
        self.rotate(ang)
    
    @property
    def is_dot(self):
        if self._x == 0 and self._y == 0:
            return True
        return False
    
    def rotate(self, angle: float | int):
        angle = math.radians(angle)
        x = copy(self._x)
        y = copy(self._y)
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        self._x = rotated_x
        self._y = rotated_y
        
        return self
    
def angle_to(pos1: list | Vec2, pos2: list | Vec2):
    normal = Vec2.two_points(vec2_to_list(pos1), vec2_to_list(pos2))
    return normal.angle

def vec2_to_list(value):
    if isinstance(value, Vec2):
        return value.xy
    elif isinstance(value, (list, tuple)):
        return value

def distance(pos1: list | Vec2, pos2: list | Vec2) -> int | float:
    pos1 = vec2_to_list(pos1)
    pos2 = vec2_to_list(pos2)
    return math.sqrt(
        (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2
    )

def center(pos1: list | Vec2, pos2: list | Vec2) -> list:
    normal = Vec2.two_points(vec2_to_list(pos1), vec2_to_list(pos2))
    normal /= 2
    pos1 -= normal
    return pos1.xy

def distance_x(pos1: list | Vec2, pos2: list | Vec2) -> int | float:
    pos1 = vec2_to_list(pos1)
    pos2 = vec2_to_list(pos2)
    return abs(pos1[0] - pos2[0])

def distance_y(pos1: list | Vec2, pos2: list | Vec2) -> int | float:
    pos1 = vec2_to_list(pos1)
    pos2 = vec2_to_list(pos2)
    return abs(pos1[1] - pos2[1])

def rect_in_rect(pos1: list | Vec2, size1: list, pos2: list | Vec2, size2: list) -> bool:
    pos1 = vec2_to_list(pos1)
    pos2 = vec2_to_list(pos2)

    center1 = [
        pos1[0] + size1[0] / 2,
        pos1[1] + size1[1] / 2
    ]
    center2 = [
        pos2[0] + size2[0] / 2,
        pos2[1] + size2[1] / 2
    ]
    x_dist = size1[0] / 2 + size2[0] / 2
    y_dist = size1[1] / 2 + size2[1] / 2

    if (distance_x(center1, center2) < x_dist and
        distance_y(center1, center2) < y_dist):
        return True
    return False

def point_in_rect(pos: list | Vec2, pos_rect: list | Vec2, size_rect: list) -> bool:
    pos = vec2_to_list(pos)
    pos_rect = vec2_to_list(pos_rect)

    if pos_rect[0]<pos[0]<pos_rect[0]+size_rect[0] and pos_rect[1]<pos[1]<pos_rect[1]+size_rect[1]:
        return True
    return False

def offset(pos: tuple[int, int], dx: int | float = 0 ,dy: int | float = 0) -> tuple[float, float]:
    return [
        pos[0] + dx,
        pos[1] + dy
    ]

def generate_dummy_2d_space(size: tuple[int, int]) -> list[list]:
    dummy = [
        [ 0 for i in range(size[0])]
        for j in range(size[1])
    ]
    return dummy

def perlin_noise(size: tuple[int, int], seeds_count: int = 1, octets: int = 1, seed = None):
    start_map = generate_dummy_2d_space(size)
    if seed is not None: random.seed(seed)
    for i in range(seeds_count):
        rx = random.randint(0, size[0] - 1)
        ry = random.randint(0, size[1] - 1)
        if start_map[rx][ry] != 1:
            start_map[random.randint(0, size[0] - 1)][random.randint(0, size[1] - 1)] = 1
        else:
            while start_map[rx][ry] != 1:
                rx = random.randint(0, size[0] - 1)
                ry = random.randint(0, size[1] - 1)
            start_map[random.randint(0, size[0] - 1)][random.randint(0, size[1] - 1)] = 1
    
    
    for i in range(octets):
        noise = generate_dummy_2d_space(size)
        for x in range(size[0]):
            for y in range(size[1]):
                if x+1==size[0]: x = -1
                if y+1==size[1]: y = -1
                
                value = 0
                value += start_map[x][y]
                value += start_map[x+1][y]
                value += start_map[x-1][y]
                value += start_map[x][y-1]
                value += start_map[x][y+1]
                value += start_map[x+1][y-1]
                value += start_map[x-1][y-1]
                value += start_map[x+1][y+1]
                value += start_map[x-1][y+1]
                value /= 9
                
                
                noise[x][y] = value

        start_map = noise

    for x in range(size[0]):
        for y in range(size[1]):
            noise[x][y] = max(min(max(0,min(((noise[x][y]+0.5)**2),1)),1),0)

    max_value = 0
    for x in range(size[0]):
        for y in range(size[1]):
            if noise[x][y]>max_value:
                max_value = noise[x][y]
    
    for x in range(size[0]):
        for y in range(size[1]):

                noise[x][y]/=max_value*1.5
    

    return noise

def normalize_noise(noise: list[list], middle_value = 0.3):
    ret_noise = []
    for y in noise:
        dn = []
        for x in y:
            if x>middle_value:
                dn.append(1)
            else:
                dn.append(0)
        ret_noise.append(dn)
    return ret_noise

def perlin_surf(size: tuple[int, int], seeds_count: int = 1, octets: int = 1, scale: int | float = 1, type='grayscale', seed: int | str | None = None) -> pygame.Surface:
    noise = perlin_noise(size, seeds_count, octets, seed)

    surf = pygame.Surface(size)
    for x in range(size[0]):
        for y in range(size[1]):
            v = noise[x][y]
            
            color = [v*255, v*255, v*255]
            if v<0.5:
                color[2] += 100
                color[2] /= 1.2
                color[0] /=2
                color[1] /= 2
            elif 0.5<v<0.52:
                color = [200,180,0]
            elif v>=0.52:
                color[1] += 50
                color[1] /= 1.5
                color[0] /= 2
                color[2]/=2
            
            surf.set_at([x,y],color)
    surf = pygame.transform.scale(surf, [surf.get_width() * scale, surf.get_height() * scale]).convert_alpha()
    return surf