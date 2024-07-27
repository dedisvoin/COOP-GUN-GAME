from src.net import *
from src.app import *
from src.window import *
from settings import *
from maps import *
from src.tilesets import *
from src.keyboard import *
from src.camera import *
from src.mouse import *
from src.functs import *
from src.shapes import shapes

screen_size = [1920, 1080]
screen_scale = 4
win_size = [screen_size[0] // screen_scale, screen_size[1] // screen_scale]
app = App(win_size, 'CGC', 
          flags=WindowFlags.SCALE,
          render_fps=False
        )

camera = Camera(app)
camera.move_delta = 0.08


load_tileset('aseprite\dirt_tile.png', 1, 16, 1)
person_sprites = load_lines_tile_animate('aseprite\person_animations.png', 2, 16, [7, 5])
print(len(person_sprites))
person_stay_anim = SpriteAnimate(convert_surfaces_to_sprites(person_sprites[0],1), 10)
person_run_anim = SpriteAnimate(convert_surfaces_to_sprites(person_sprites[1],1), 3)
person_stay_anim.start()
person_run_anim.start()

client = Client(CONNECT_IP)
client.connect()


this_game_map = []
game_map_loaded = False
this_map_surf = None
person_poses = []
person_dirs = []
person_moveds = []
keyboard_preses = [
    False, False, False
]
used_gun = None
person_pos = [0, 0]
person_click = False
click_timer = 0
all_bullets = []


def get_this_game_map(data):
    global this_game_map, game_map_loaded, this_map_surf
    try:
        if not game_map_loaded:
            this_game_map = all_maps[data['game_map']]
            game_map_loaded = True
            this_map_surf = render_tilemap_from_2d_space(delete_spawns(this_game_map), 16, 1, True)
    except: ...


def create_client_send_data():
    used_gun_timer = 1
    for gun in guns:
        if gun.name == used_gun:
            used_gun_timer = gun.shoot_time
    send_data = [
        Packet(keyboard_preses, 'key_presses').get(),
        Packet([angle_to(mouse_.pos, person_pos), used_gun, mouse_.pos[0]<person_pos[0], person_click, click_timer%used_gun_timer==0], 'gun_data').get(),
    ]
    return send_data

@NetProcess()
def client_precess():
    global person_poses, person_dirs, person_moveds, all_bullets
    while True:
        tick(0.01)
        client.sended_data = create_client_send_data()

        client.send_all()
        client.recv_all(4000)
        
        person_poses = client.recv_data['player_pos']
        person_dirs = client.recv_data['player_dir']
        person_moveds = client.recv_data['player_move']
        all_bullets = client.recv_data['bullets']
        
        get_this_game_map(client.recv_data)










load_font_by_file('pixel_font','fonts\smallest_pixel-7.ttf', 10)



inventory_size = [16*4, app.size[1]]
inventory_pos = [-inventory_size[0],0]
inventory_surf = pygame.Surface(inventory_size).convert_alpha()
inventory_surf.set_alpha(100)
inventory_open = False



class InventoryObj:
    def __init__(self, name, pos, img) -> None:
        self.pos = pos
        self.sprite = Sprite.load_sprite(img)
        self.size = self.sprite.start_image.get_size()
        self.at_pos = pos
        self.name = name

    def render(self):
        global used_gun
        self.at_pos = [self.pos[0]+inventory_pos[0]+4, self.pos[1]+10]
        shapes.rect(app.surf, self.at_pos, self.sprite.start_image.get_size(), (100,100,100), width=0)
        self.sprite.pos = [self.at_pos[0]+self.sprite.start_image.get_size()[0]/2, self.at_pos[1]+self.sprite.start_image.get_size()[1]/2]
        self.sprite.render(app.surf)
        shapes.rect(app.surf, self.at_pos, self.sprite.start_image.get_size(), (200,200,200), width=1)
        if self.name == used_gun:
            shapes.rect(app.surf, self.at_pos, self.sprite.start_image.get_size(), (200,200,100), width=1)

        if point_in_rect(mouse_.pos, self.at_pos, self.size):
            shapes.rect(app.surf, self.at_pos, self.sprite.start_image.get_size(), (255,255,255), width=2)
            if mouse_.press(Mouse.Button.BTN_LEFT):
                used_gun = self.name


inventory_objects = [
    InventoryObj('Start Gun', [0, 0], 'aseprite\guns\standart_gun\standart_gun.png')
]


def render_gun_display():
    global inventory_open
    #shapes.rect(app.surf, inventory_pos, inventory_size, (10, 10, 10) )
    app.surf.blit(inventory_surf, inventory_pos)
    render_font(app.surf, 'pixel_font', 'Invenory', (100,100,100), [3, 0])
    if point_in_rect(mouse_.pos, [0, 0], [40,10]):
        render_font(app.surf, 'pixel_font', 'Invenory', (200,200,200), [3, 0])
        if mouse_.click(Mouse.Button.BTN_LEFT):
            inventory_open = not inventory_open

    if inventory_open:
        if inventory_pos[0]<-5:
            inventory_pos[0]+=5 
    
    if not inventory_open:
        if inventory_pos[0]>-inventory_size[0]:
            inventory_pos[0]-=5 

    if inventory_pos[0]>-inventory_size[0]+5:
        for obj in inventory_objects:
            obj.render()
            
            



    
    
class Gun:
    def __init__(self, sprite, name, dy=0, shoot_time = 100) -> None:
        self.sprite = Sprite.load_sprite(sprite)
        self.name = name
        self.dy = dy
        self.shoot_time = shoot_time

    def render(self, player_pos, angle, mir=False):
        self.sprite.pos = [player_pos[0], player_pos[1]+self.dy]
        self.sprite.angle = angle-180
        self.sprite.mirror_y = mir
        
            

        self.sprite.render(app.surf)
        

guns = [
    Gun('aseprite\guns\standart_gun\standart_gun_in_hend.png', 'Start Gun', 3, 10)
]




@AppProcess(app, True)
def main(delta):
    global person_click, click_timer
    global keyboard_preses, person_pos

    for i, pos in enumerate(person_poses):
        if str(pos[1]) == str(client.id):
            camera.target_pos = pos[0]
            person_pos = [pos[0][0]+camera.pos[0],pos[0][1]+camera.pos[1]]
    try:
        camera.update()
    except: ...

    if this_map_surf is not None:
        app.surf.blit(this_map_surf, [camera.pos[0], camera.pos[1]])
    person_stay_anim.update()
    person_run_anim.update()


    for i, pos in enumerate(person_poses):
        try:

            
            person_stay_anim.pos = [pos[0][0]+camera.pos[0],pos[0][1]+camera.pos[1]]
            person_run_anim.pos = [pos[0][0]+camera.pos[0],pos[0][1]+camera.pos[1]]
            if person_moveds[i]:
                person_run_anim.mirror_x = person_dirs[i]
                person_run_anim.render(app.surf)
            else:
                person_stay_anim.mirror_x = person_dirs[i]
                person_stay_anim.render(app.surf)
            for gun in guns:
                
                if gun.name == pos[2]:
                    
                    gun.render([pos[0][0]+camera.pos[0],pos[0][1]+camera.pos[1]], pos[3], pos[4])
        except: ...

    
    keyboard_preses = [
        keyboard_.press('left'),
        keyboard_.press('right'),
        keyboard_.press('up'),
    ]
    
    person_click = mouse_.press(Mouse.Button.BTN_LEFT)
    click_timer += 1
    if click_timer==1000:click_timer = 0



    for bullet in all_bullets:
        pos = [bullet[1][0]+camera.pos[0], bullet[1][1]+camera.pos[1]]
        shapes.circle(app.surf, pos, 3, 'red')



    render_gun_display()

    
    



app.run()