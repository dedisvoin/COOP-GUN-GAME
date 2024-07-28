from src.functs import *
from src.shapes import *

import pygame


##################################################################################################
#                            BOX COLLIDEING ENGINE (V2.8 OPTIMEZED)                              #
##################################################################################################


ENGINE_GRAVITY = Vec2(0, 0.98)

class BoxColliderTypes:
    STATICK = 'STATICK'
    DYNAMIC = 'DYNAMIC'


class BoxCollider:
    def __init__(self, 
                 id: str | int,
                 pos: tuple[int, int], 
                 size: tuple[int, int], 
                 type: BoxColliderTypes = BoxColliderTypes.STATICK, 
                 _start_speed: Vec2 = Vec2(0, 0),
                 _resistance: Vec2 = Vec2(1, 1),
                 _air_resistance: Vec2 = Vec2(1, 1),
                 _bounce: Vec2 = Vec2(1, 1),
                 _gravity: Vec2 = ENGINE_GRAVITY
                 ) -> 'BoxCollider':
        
        
        self.__id = id
        self.pos = Vec2(*pos)
        self.speed = _start_speed
        self.size = size
        self.__gravity = _gravity
        self.__resistance = _resistance
        self.__air_resistance = _air_resistance
        self.__type = type
        self.__center = [0, 0]
        self.__bounce = _bounce
        self.collidings = {
            'up': False,
            'down': False,
            'left': False, 
            'right': False
        }

    

    def update(self):
        self.__center = [
            self.pos.x + self.size[0] / 2,
            self.pos.y + self.size[1] / 2
        ]
        self.collidings = {
            'up': False,
            'down': False,
            'left': False, 
            'right': False
        }

    @property
    def air_resistance(self):
        return self.__air_resistance

    @property
    def gravity(self):
        return self.__gravity

    @property
    def id(self): return self.__id

    @property
    def bounce(self): return self.__bounce

    @property
    def type(self): return self.__type

    @property
    def center(self): return self.__center

    @property
    def resistance(self): return self.__resistance

    @property
    def up(self):
        return self.pos.y
    
    @property
    def down(self):
        return self.pos.y + self.size[1]
    
    @property
    def left(self):
        return self.pos.x
    
    @property
    def right(self):
        return self.pos.x + self.size[0]
    
    @up.setter
    def up(self, value):
        self.pos.y = value

    @down.setter
    def down(self, value):
        self.pos.y = value - self.size[1]

    @left.setter
    def left(self, value):
        self.pos.x = value

    @right.setter
    def right(self, value):
        self.pos.x = value - self.size[0]
    

class BoxColliderManager:
    def __init__(self) -> None:
        self.__colliders: list[BoxCollider] = []
        self.__end_colliders: list[BoxCollider] = []

        self.__statick_colliders: list[BoxCollider] = []
        self.__dynamic_colliders: list[BoxCollider] = []

    def get(self, id: int | str) -> BoxCollider:
        for collider in self.__colliders:
            if collider.id == id: return collider

    def statick_colliders_count(self) -> int:
        return len(self.__statick_colliders)
    
    def dynamic_colliders_count(self) -> int:
        return len(self.__dynamic_colliders)

    def add(self, box_collider: BoxCollider):
        self.__colliders.append(box_collider)

    def adds(self, box_colliders: list[BoxCollider]):
        self.__colliders += box_colliders

    def split(self) -> tuple[list[BoxCollider], list[BoxCollider]]:
        staticks, dynamics = [], []

        for collider in self.__colliders:
            if collider.type == BoxColliderTypes.STATICK:
                staticks.append(collider)
            elif collider.type == BoxColliderTypes.DYNAMIC:
                dynamics.append(collider)

        return staticks, dynamics
    
    def render(self, surf: pygame.Surface):
        for collider in self.__colliders:
            shapes.rect(surf, collider.pos.xy, collider.size, width=1, color='red')

    def pos_in_colliders(self, pos: list):
        for collider in self.__statick_colliders:
            if point_in_rect(pos, collider.pos.xy, collider.size): return True
        return False

    def collide_y(self, collider: BoxCollider):
        for statick_collider in self.__statick_colliders:
            if rect_in_rect(collider.pos.xy, collider.size, statick_collider.pos.xy, statick_collider.size):
                if collider.center[1] < statick_collider.center[1]:
                    collider.down = statick_collider.up
                    collider.speed.y *= -(statick_collider.bounce.y + collider.bounce.y) / 2
                    collider.collidings['down'] = True
                    

                if collider.center[1] > statick_collider.center[1]:
                    collider.up = statick_collider.down
                    collider.speed.y *= -(statick_collider.bounce.y + collider.bounce.y) / 2
                    collider.collidings['up'] = True

                collider.speed.x *= (collider.resistance.x + statick_collider.resistance.x) / 2


    def collide_x(self, collider: BoxCollider):
        for statick_collider in self.__statick_colliders:
            if rect_in_rect(collider.pos.xy, collider.size, statick_collider.pos.xy, statick_collider.size):
                if collider.center[0] < statick_collider.center[0]:
                    collider.right = statick_collider.left
                    collider.speed.x *= -(statick_collider.bounce.x + collider.bounce.x) / 2
                    collider.collidings['right'] = True

                elif collider.center[0] > statick_collider.center[0]:
                    collider.left = statick_collider.right
                    collider.speed.x *= -(statick_collider.bounce.x + collider.bounce.x) / 2
                    collider.collidings['left'] = True
        
    
    def update(self):
        for collider in self.__colliders:
            collider.update()

        if self.__end_colliders != self.__colliders:
            self.__statick_colliders, self.__dynamic_colliders = self.split()

        for collider in self.__dynamic_colliders:
            
            collider.speed += collider.gravity
            collider.speed.x *= collider.air_resistance.x
            collider.speed.y *= collider.air_resistance.y
            

            collider.pos.y += collider.speed.y

            self.collide_y(collider)

            collider.pos.x += collider.speed.x

            self.collide_x(collider)

        self.__end_colliders = copy(self.__colliders)

    def get_all_dyn_center(self) -> list[list]:
        return [coll.center for coll in self.__dynamic_colliders]
                

def list_to_collider_map(map_list: list[list], tile_size = 16, bounce = Vec2(0, 0)) -> list[BoxCollider]:
    dummy_map = [copy(dm) for dm in map_list]
    colliders = []
    
    for y in range(len(dummy_map)):
        for x in range(len(dummy_map[y])):
            if dummy_map[y][x] != 0:
                min_height = 10 ** 6
                width = 0
                height = 0
                
                while dummy_map[y][x + width]!=0:
                    height = 0
                    while dummy_map[y + height][x + width]!=0:
                        height += 1
                    min_height = min(height, min_height)
                    width += 1
                
                for ry in range(0, min_height):
                    for rx in range(0, width):
                        dummy_map[y + ry][x + rx] = 0
                
                colliders.append(BoxCollider('none', [x * tile_size, y * tile_size], [width * tile_size, min_height * tile_size], _bounce = bounce))
    
    return colliders

        

                        
                        

    