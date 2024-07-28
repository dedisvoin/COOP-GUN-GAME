import random
from typing import Dict
import pygame
from src.img import *

tilesets = {}

def load_tileset(file_name: str, id: int | str, tile_size: int = 16, scale: float | int = 1):
    global tilesets
    t = TileSet(file_name, tile_size, scale, id)
    t.cutting()
    tilesets[id] = t

def load_tileset_from_surf(surface: pygame.Surface, id: int | str, tile_size: int = 16, scale: float | int = 1):
    global tilesets
    t = TileSet.from_surface(surface, tile_size, scale, id)
    t.cutting(True)
    tilesets[id] = t


class TileSet:
    def __init__(self, file_name: str = None, tile_size: int = 16, scale: float | int = 1, id: int | str = None) -> None:
        self.file_name = file_name
        self.tile_size = tile_size
        self.scale = scale
        self.id = id
        if self.file_name is not None:
            self.image = pygame.image.load(self.file_name)
        else:
            self.image = None
        self.cuts: Dict[str, Sprite | None] = {

            'ul': None,
            'ur': None,
            'u': None,

            'm': None,
            'ml': None,
            'mr': None,

            'd': None,
            'dl': None,
            'dr': None,

            'o': None,

            'vu': None,
            'v': None,
            'vd':None,

            'hl': None,
            'h': None,
            'hr': None,

            'mdr': None,
            'mdl': None,
            'mur': None,
            'mul': None,
            'mudlr': None

        }

    @classmethod
    def from_surface(self, surface: pygame.Surface, tile_size: int = 16, scale: float | int = 1, id: int | str = None) -> 'TileSet':
        ts = TileSet(tile_size=tile_size, scale=scale, id=id)
        ts.image = surface
        return ts

    def image_clear(self, img: pygame.Surface,):
        color = ''
        for i in range(0, 10):
            c = img.get_at([random.randint(0, self.tile_size - 1), random.randint(0, self.tile_size - 1)])
            color += f'{c[0]}{c[1]}{c[2]}'
        if len(set(color)) == 1:
            return True
        return False

    def cutting(self, not_clear = False):
        tiles_w = 4
        tiles_h = 7

        sprites = []

        for h in range(tiles_h):
            for w in range(tiles_w):
                pos = [w * self.tile_size, h * self.tile_size]
                surf = self.image.subsurface(pos, [self.tile_size, self.tile_size])
                if not self.image_clear(surf) or not_clear:
                    sprites.append(surf)
        
        

        self.cuts['ul'] = sprites[0]
        self.cuts['u'] = sprites[1]
        self.cuts['ur'] = sprites[2]
        self.cuts['vu'] = sprites[3]

        self.cuts['ml'] = sprites[4]
        self.cuts['m'] = sprites[5]
        self.cuts['mr'] = sprites[6]
        self.cuts['v'] = sprites[7]

        self.cuts['dl'] = sprites[8]
        self.cuts['d'] = sprites[9]
        self.cuts['dr'] = sprites[10]
        self.cuts['vd'] = sprites[11]

        self.cuts['hl'] = sprites[12]
        self.cuts['h'] = sprites[13]
        self.cuts['hr'] = sprites[14]
        self.cuts['o'] = sprites[15]

        self.cuts['mdr'] = sprites[16]
        self.cuts['mdl'] = sprites[17]
        self.cuts['mudlr'] = sprites[18]
        self.cuts['mulr'] = sprites[19]        

        self.cuts['udr'] = sprites[20]
        self.cuts['udl'] = sprites[21]
#       self.cuts['NONE'] = sprites[NONE]
        self.cuts['mdlr'] = sprites[23]

        self.cuts['cul'] = sprites[24]
        self.cuts['cur'] = sprites[25]
        

        for tile_name in self.cuts:
            if self.cuts[tile_name] is not None:
                self.cuts[tile_name] = Sprite.load_surf(self.cuts[tile_name])
                self.cuts[tile_name].scale = self.scale

    @property
    def get(self):
        return self.cuts

def render_tilemap_from_2d_space(space: list[list], tile_size: int = 16, map_scale: float = 1, connect_all: bool = True):
    space_width = len(space[0])
    space_height = len(space)
    tile_size = int(tile_size)
    
    space_surf = pygame.Surface([space_width * tile_size, space_height * tile_size]).convert()
    space_surf.set_colorkey((0,0,0))

    



    for y in range(space_height):
        for x in range(space_width):
            
            if y==space_height-1: y = -1
            if x==space_width-1: x = -1

            tile = None
            id = space[y][x]

            up = space[y-1][x]
            down = space[y+1][x]
            left = space[y][x-1]
            right = space[y][x+1]
            up_left = space[y-1][x-1]
            down_left = space[y+1][x-1]
            up_right = space[y-1][x+1]
            down_right = space[y+1][x+1]


            if space[y][x] != 0:
                
                if up!=id and down==id:
                    tile = tilesets[id].get['u']
                    if left!=id and right!=id:
                        tile = tilesets[id].get['vu']
                    if left==id and right!=id:
                        tile = tilesets[id].get['ur']
                    if left!=id and right==id:
                        tile = tilesets[id].get['ul']
                    
                elif up==id and down==id:
                    tile = tilesets[id].get['m']
                    if left!=id and right!=id:
                        tile = tilesets[id].get['v']
                    if left==id and right!=id:
                        tile = tilesets[id].get['mr']
                    if left!=id and right==id:
                        tile = tilesets[id].get['ml']
                    if left==id and right==id:
                        
                        if up_left!=id and down_right!=id and up_right==id and down_left==id:
                            tile=tilesets[id].get['cul']
                        if up_left==id and down_right==id and up_right!=id and down_left!=id:
                            tile=tilesets[id].get['cur']

                elif up==id and down!=id:
                    tile = tilesets[id].get['d']
                    if left!=id and right!=id:
                        tile = tilesets[id].get['vd']
                    if left==id and right!=id:
                        tile = tilesets[id].get['dr']
                    if left!=id and right==id:
                        tile = tilesets[id].get['dl']

                elif up!=id and down!=id:
                    tile = tilesets[id].get['h']
                    if left==id and right!=id:
                        tile = tilesets[id].get['hr']
                    if left!=id and right==id:
                        tile = tilesets[id].get['hl']
                    
                if up==id and down==id and left==id and right==id:
                    if up_left==id and up_right==id:
                        if down_left!=id and down_right==id:
                            tile = tilesets[id].get['udr']
                        elif (down_left==id and down_right!=id):
                            tile = tilesets[id].get['udl']
                        elif down_left!=id and down_right!=id:
                            tile = tilesets[id].get['mdlr']
                    
                    if down_left==id and down_right==id:
                        if up_left!=id and up_right==id:
                            tile = tilesets[id].get['mdr']

                        elif up_left==id and up_right!=id:
                            tile = tilesets[id].get['mdl']

                        elif up_left!=id and up_right!=id:
                            tile = tilesets[id].get['mulr']

                    if down_left!=id and down_right!=id and up_left!=id and up_right!=id:
                        tile = tilesets[id].get['mudlr']

                


            if tile is not None:
                tile.to_size([tile_size, tile_size])
                space_surf.blit(tile.new_image, [x*tile_size, y*tile_size])

    
    return pygame.transform.scale(space_surf, [space_surf.get_width()*map_scale, space_surf.get_height()*map_scale])

