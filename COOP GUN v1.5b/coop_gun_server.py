from src.net import *
from src.engine import *
from src.functs import *
from settings import *
from maps import *
from src.app import *
from guns import all_guns_bullets

player_collider_size = [6, 14]
players = []
class Player:
    def __init__(self, id) -> None:
        global spawn_poses, collider_manager
        self.id = id
        self.start_pos = random.choice(spawn_poses)
        #del spawn_poses[spawn_poses.index(self.start_pos)]
        print(self.start_pos)

        self.collider = BoxCollider(self.id, copy(self.start_pos), player_collider_size, BoxColliderTypes.DYNAMIC, 
                                    _gravity = Vec2(0, 0.3), _resistance = Vec2(0.5,0.5), _bounce = Vec2(0.1,0.1), _air_resistance = Vec2(0.99,1))
        GM.CM.add(self.collider)
        self.direction = False
        self.moved = False
        self.player_gun_angle = 0
        self.used_gun = None
        self.gun_mir = False
        self.hp = 100

class Game:
    def __init__(self) -> None:
        self.CM = BoxColliderManager()
        self.CM.adds(list_to_collider_map(delete_spawns(this_game_map), TILE_SIZE, Vec2(0, 0)))

map_index = random.randint(0, len(all_maps)-1)
this_game_map = all_maps[map_index]
spawn_poses = get_spawn_poses_to_map(this_game_map)
GM = Game()
server = Server(CONNECT_IP)
all_bullets = []


def send_packet_forming():

    send_packet = []
    send_packet.append(Packet(map_index, 'game_map').get())
    send_packet.append(Packet([[[int(player.collider.center[0]), int(player.collider.center[1])], player.id, player.used_gun, int(player.player_gun_angle), player.gun_mir, player.hp] for player in players], 'player_pos').get())
    send_packet.append(Packet([player.direction for player in players], 'player_dir').get())
    send_packet.append(Packet([player.moved for player in players], 'player_move').get())
    send_packet.append(Packet([
        [bullet[0], bullet[1].xy, bullet[2].xy]
        for bullet in all_bullets
    ], 'bullets').get())

    return send_packet


@NetProcess()
def wait_connects():
    global players
    while True:
        tick(SPEED)
        server.wait_connets()

        
        if server.event_connect:
            connected_client_id = server.event_connect_data[0]
            players.append(Player(connected_client_id))


@NetProcess()
def check_connects():
    while True:
        tick(SPEED)
        server.check_clients()

        if server.event_disconnect:
            disconnected_client_id = server.event_disconnect_data[0]
            del players[players.index(list(filter(lambda player: player.id == disconnected_client_id, players))[0])]


@NetProcess()
def server_process():
    while True:
        tick(SPEED)


        server.recv_all()

        server.sended_data = send_packet_forming()

        

        server.send_all()
        

app = App(size=[230,20],title='Server')
app.set_exit_key('tab')

def players_movement():
    global all_bullets
    for player in players:
        player.moved = False
        player.collider.speed.y = min(player.collider.speed.y, 4)
    for id in server.recv_data:
        try:
            data = server.recv_data[id]
            
            
            for player in players:
                
                if str(player.id) == str(id):
                    
                    player.gun_mir = data[1][1][2]
                    player.used_gun = data[1][1][1]
                    player.player_gun_angle = data[1][1][0]
                    if data[0][1][0] == True:
                        player.collider.speed.x = -2
                        player.direction = True
                        player.moved = True
                    if data[0][1][1] == True:
                        player.collider.speed.x = 2
                        player.direction = False
                        player.moved = True
                    if data[0][1][2] == True and player.collider.collidings['down']:
                        player.collider.speed.y = -7 
                    
                    shoot = data[1][1][1] != None
                    
                    if shoot == True:
                        
                        bullet_information = all_guns_bullets[data[1][1][1]]
                        
                        

                        if data[1][1][3] and data[1][1][4]:
                            
                            speed = Vec2(0,100)
                            
                            speed.normalize_at()
                            
                            
                            speed.angle = data[1][1][0]
                            
                            speed*=bullet_information[1]
                            
                            create_bullet(data[1][1][1], [player.collider.center[0], player.collider.center[1]-3], speed, player.id)
                
        except:...


def create_bullet(gun_name, pos, speed, pi):
    global all_bullets
    
    all_bullets.append([
        gun_name, Vec2(*pos), speed, 0, pi
    ])

def bullets_update():
    global all_bullets
    for bullet in all_bullets:
        bullet[1] += bullet[2]
        bullet[3] += 1
        if bullet[3] > 300:
            del all_bullets[all_bullets.index(bullet)]
            break
        if GM.CM.pos_in_colliders(bullet[1].xy):
            del all_bullets[all_bullets.index(bullet)]
            break

        for player in players:
            if point_in_rect(bullet[1].xy, player.collider.pos.xy, player.collider.size) and player.id != bullet[4]:
                player.hp-=10
                del all_bullets[all_bullets.index(bullet)]
                break
    
    for player in players:
        if player.hp<=0:
            del players[players.index(player)]
            break


@AppProcess(app, True)
def main(delta):   


    #tick(0.01)
    GM.CM.update()


    GM.CM.render(app.surf)
    players_movement()
    bullets_update()

    for bullet in all_bullets:
        shapes.circle(app.surf, bullet[1].xy, 4, 'red')

    
    
app.run()
        