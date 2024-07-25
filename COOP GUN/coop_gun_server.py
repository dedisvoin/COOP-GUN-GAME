from src.engine import *
from src.net import *
from settings import TILE_SIZE
import random



MAP_1 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]
MAPS = [MAP_1]

def choise_random_map(maps):
    return MAPS[random.randint(0, len(maps) - 1)]

THIS_GAME_MAP = choise_random_map(MAPS)

COLLIDER_MANAGER = BoxColliderManager()
COLLIDERS = list_to_collider_map(THIS_GAME_MAP, TILE_SIZE, Vec2(0, 0))
COLLIDER_MANAGER.adds(COLLIDERS)

##################################################################
#                      PLAYER CONSTRUCTER         
##################################################################

PERSON_USING_SPAWN_POSEES = []
PERSON_COLLIDER_SIZE = [10, 13]

spawn_positions = []
for y in range(len(THIS_GAME_MAP)):
    for x in range(len(THIS_GAME_MAP[y])):
        if THIS_GAME_MAP[y][x] == 9:
            spawn_positions.append([x, y])
            THIS_GAME_MAP[y][x] = 0

print('Spawns created:', spawn_positions)

players = []
class Player:
    def __init__(self, id: int | str) -> None:
        global COLLIDER_MANAGER
        self.start_position = self.generate_start_position_from_map()
        print(self.start_position)
        self.id = id
        self.collider = BoxCollider(self.id, self.start_position, PERSON_COLLIDER_SIZE, BoxColliderTypes.DYNAMIC, _resistance = Vec2(0.5, 1), _bounce = Vec2(0, 0.1))
        COLLIDER_MANAGER.add(self.collider)
        self.on_dirt = False
        self.direction = False
        

    def generate_start_position_from_map(self) -> tuple[int, int]:
        global PERSON_USING_SPAWN_POSEES
        this_person_spawn_pos = self.choise_spawn_pos(spawn_positions)
        if this_person_spawn_pos in PERSON_USING_SPAWN_POSEES:
            while this_person_spawn_pos in PERSON_USING_SPAWN_POSEES:
                this_person_spawn_pos = self.choise_spawn_pos(spawn_positions)
        PERSON_USING_SPAWN_POSEES.append(this_person_spawn_pos)

        return [this_person_spawn_pos[0]*TILE_SIZE, this_person_spawn_pos[1]*TILE_SIZE]
    
    def choise_spawn_pos(self, spawn_positions):
        return spawn_positions[random.randint(0, len(spawn_positions) - 1)]
    
    def update(self):
        self.on_dirt = False
        if self.collider.collidings['down']:
            self.on_dirt = True
    
    
##################################################################
#                      PLAYER CONSTRUCTER         
################################################################## 
        

##################################################################
#                        SERVER PROCESS         
################################################################## 


    

def generate_send_packets():
    send_packets = [
        Packet(len(players), 'online_players_count').get(),
        
    ]
    if all_clients_recv_game_map<2:
        send_packets.append(Packet(THIS_GAME_MAP, 'game_map').get())
    else:
        send_packets.append(Packet([player.collider.center for player in players], 'player_poses').get())
    
    return send_packets

start_sending = False
all_clients_recv_game_map = 0
def run_server():
    
    server = Server()

    @NetProcess()
    def server_connects_check():
        global players
        while True:
            tick(0.01)
            server.check_clients()

            # delete disconnected clients --------------------------------
            if server.event_disconnect:
                disconnected_client_id = server.event_disconnect_data[0]
                for player in players:
                    if player.id == disconnected_client_id:
                        del players[players.index(player)]
                        break
            # delete disconnected clients --------------------------------

    @NetProcess()
    def updates():
        global COLLIDER_MANAGER, players
        while True:
            tick(0.01)
            COLLIDER_MANAGER.update()
            for player in players:
                player.update()

    @NetProcess()
    def wait_connects():
        global players, start_sending
        while len(players) < 2:
            tick(0.01)
            server.wait_connets()

            ##################################################################
            #                   CREATE PLAYER OBJECT
            ##################################################################

            if server.event_connect:
                connected_client_id = server.event_connect_data[0]
                players.append(Player(connected_client_id))
                print(len(players))
                

            ##################################################################
            #                   CREATE PLAYER OBJECT
            ##################################################################
    
        start_sending = True
    
        print(start_sending)
            
    @NetProcess()
    def server_process():
        global start_sending, all_clients_recv_game_map

        while start_sending == False:    tick(0.01)

        while True:
            tick(0.01)
                ##################################################################
                #                        SEND INFORMATION
                ##################################################################

            server.sended_data = generate_send_packets()
            for id in server.recv_data:
                if server.recv_data[id][0][1] == True:
                    all_clients_recv_game_map += 1

                ##################################################################
                #                        SEND INFORMATION
                ##################################################################


                    
            server.recv_all()
            server.send_all()
            
    

run_server()
##################################################################
#                        SERVER PROCESS         
################################################################## 