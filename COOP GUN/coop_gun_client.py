from src.window import *
from src.app import *
from src.mouse import *
from src.keyboard import *
from src.events import *
from src.tilesets import *
from src.img import *
from src.net import *


##################################################################
#                          WINDOW CREATE
##################################################################
APP_WINDOW_SIZE = [1920, 1080]
APP_SCREEN_SCALE = 4
APP_SCREEN_SIZE = [APP_WINDOW_SIZE[0] // 4, APP_WINDOW_SIZE[1] // 4]

app = App(
    size = APP_SCREEN_SIZE,
    title = 'COOP GUN',
    flags = WindowFlags.SCALE | WindowFlags.RESIZE,
    render_fps = True
)
##################################################################
#                          WINDOW CREATE
##################################################################

##################################################################
#                           LOAD DATAS
##################################################################
load_tileset('aseprite\dirt_tile.png', 1, 16, 1)
person_sprites = load_lines_tile_animate('aseprite\person_animations.png', 2, 16, [7, 5])
person_stay_anim = SpriteAnimate(convert_surfaces_to_sprites(person_sprites[0], 1), 5)
person_move_anim = SpriteAnimate(convert_surfaces_to_sprites(person_sprites[1], 1), 5)
##################################################################
#                           LOAD DATAS
##################################################################

##################################################################
#                            GAME MAP
##################################################################
THIS_GAME_MAP = []
GAME_MAP_SURF = None
##################################################################
#                            GAME MAP
##################################################################

##################################################################
#                          CLENT CREATE
##################################################################


def generate_send_packet():
    map_loaded = False
    if THIS_GAME_MAP!=[]:
        map_loaded = True

    send_packets = [
        Packet(map_loaded, 'map_loaded').get()
    ]
    return send_packets


def client_start():
    global THIS_GAME_MAP
    client = Client()
    client.connect()
    
    @NetProcess()
    def client_process():
        global THIS_GAME_MAP, GAME_MAP_SURF, CLIENT_DATAS

        while True:
            tick(0.01)



            client.sended_data = generate_send_packet()


            client.send_all()
            client.recv_all(1024*10)

            try:
                if client.recv_data['game_map']!=[] and THIS_GAME_MAP == []:
                    THIS_GAME_MAP = client.recv_data['game_map']
                    GAME_MAP_SURF = render_tilemap_from_2d_space(THIS_GAME_MAP, 16, 1)  
            except: ...

            try:
                CLIENT_DATAS['poses'] = client.recv_data['player_poses']
            except: ...


                

            
            
##################################################################
#                          CLENT CREATE
##################################################################









CLIENT_DATAS = {
    'poses': None
}




##################################################################
#                            GAME LOOP
##################################################################
client_start()

@AppProcess(app, True)
def main(delta):
    if GAME_MAP_SURF is not None:
        app.surf.blit(GAME_MAP_SURF, [0, 0])

    if CLIENT_DATAS['poses'] is not None:
        for pos in CLIENT_DATAS['poses']:
            person_stay_anim.pos = pos
            person_stay_anim.render(app.surf)
##################################################################
#                            GAME LOOP
##################################################################


app.run()