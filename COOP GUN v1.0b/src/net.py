from src.constants import SERVER_LOCAL_HOST, SERVER_LOCAL_PORT
from colorama import Fore, Style
from ast import literal_eval
from threading import Thread
from time import sleep
import platform
import socket
import random
import time


# Этот метод позволяет замораживать сетевой процесс (нужен для регулирования скорости отправки данных)
def tick(sec):
    sleep(sec)

NetDebug = True

def set_net_debug_status(value: bool = False):
    global NetDebug
    NetDebug = value

# Декоратор создающий процессы связанные с сетью
def NetProcess():
    def inner(funct):
        Thread(target=funct).start()
        return None
    return inner

# Класс дебага (УДОБНО)
class debug:
    @classmethod
    def NetDebug(self):
        if NetDebug:
            print(f'{Style.BRIGHT}{Fore.MAGENTA}[ {time.gmtime(time.time()).tm_hour}:{time.gmtime(time.time()).tm_min}:{time.gmtime(time.time()).tm_sec} ]{Style.RESET_ALL}{Fore.RESET} Net-Deubug')

    @classmethod
    def Line(self):
        return f'  {Fore.MAGENTA}{Style.BRIGHT}| >{Fore.RESET}{Style.RESET_ALL}'
    
    @classmethod
    def Succes(self):
        return f'{Fore.GREEN}[ OK ]{Fore.RESET}'
    
    @classmethod
    def Error(self):
        return f'{Fore.RED}[ ERROR ]{Fore.RESET}'
    
    @classmethod
    def Warning(self):
        return f'{Fore.YELLOW}[ WARNING ]{Fore.RESET}'

    @classmethod
    def ServerCreateDebug(self, host, port, mcc):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} {self.Succes()} Server created {Fore.BLUE}({host=}, {port=}){Fore.RESET}')
            my_system = platform.uname()
            print(f"{self.Line()} {Fore.YELLOW}System:{Fore.GREEN} {my_system.system}")
            print(f"{self.Line()} {Fore.YELLOW}Node Name:{Fore.GREEN} {my_system.node}")
            print(f"{self.Line()} {Fore.YELLOW}Release:{Fore.GREEN} {my_system.release}")
            print(f"{self.Line()} {Fore.YELLOW}Version:{Fore.GREEN} {my_system.version}")
            print(f"{self.Line()} {Fore.YELLOW}Machine:{Fore.GREEN} {my_system.machine}{Fore.RESET}")
            print(f"{self.Line()} {Fore.YELLOW}Max Clients Count:{Fore.GREEN} {mcc}{Fore.RESET}")

    @classmethod
    def ServerClientDisconected(self, host, port, cc, mcc):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} {self.Warning()} Client disconnected {Fore.BLUE}({host=}, {port=}){Fore.RESET}')
            if mcc!=None:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / {mcc}{Fore.RESET}')
            else:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / Infinity{Fore.RESET}')

    @classmethod
    def ServerClientSleep(self, host, port, errc):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} {self.Warning()} Client sleeped {Fore.BLUE}({host=}, {port=}){Fore.RESET} {Fore.RED}ticks ( {errc} / 5 ){Fore.RESET} ')

    @classmethod
    def ServerWaitedDebug(self):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} Server waited connects...')

    @classmethod
    def ServerAcceptConnect(self, addr, id, cc, mcc):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} {self.Succes()} Client connected {Fore.BLUE}({addr=}){Fore.RESET} {Fore.CYAN}({id=}){Fore.RESET}')
            if mcc!=None:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / {mcc}{Fore.RESET}')
            else:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / Infinity{Fore.RESET}')

    @classmethod
    def ClientConnectDebug(self, host, port):
        self.NetDebug()
        print(f'{self.Line()} {self.Succes()} Connected {Fore.BLUE}({host=}, {port=}){Fore.RESET}')

    @classmethod
    def ServerClientsMaxed(self, host, port, cc, mcc):
        if NetDebug:
            self.NetDebug()
            print(f'{self.Line()} {self.Error()} Error connect {Fore.BLUE}({host=}, {port=}){Fore.RESET}')
            if mcc!=None:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / {mcc}{Fore.RESET}')
            else:
                print(f'{self.Line()} {Fore.YELLOW}Client count:{Fore.GREEN} {cc} / Infinity{Fore.RESET}')

# Вспомогательный дата класс пакета данных
class Packet:
    def __init__(self, data: list, name: str) -> None:
        self.data = [name, data]
        #self.size = len(data)
        #self.name = name

    def get(self):
        return self.data

# Класс-каркасс для создания более продвинутых сетевых узлов (только стримящих даннные)
class Net:
    def __init__(self, host: str = SERVER_LOCAL_HOST, port: int = SERVER_LOCAL_PORT) -> None:
        self.port = port
        self.host = host
        self.init()
    
    def init(self):
        self.net = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Класс сервера (узла) соединяющего все остальные узлы в одну сеть
# - Может за раз рассылять пакеты всем подключенным узлам не используя оперативную память компьютера для сохранения буфера
# - Может принимать пакеты отправленные от клиентов (за раз до нескольких тысяч пакетов)
# - Имеется возможность отслеживать получаемые пакеты (узнавать кто именно отправил данный пакет)
# - Четкий контроль за состояниями клиентов (находятся ли они онлайн или-же отключены)

class Server(Net):
    def __init__(self, host: str = SERVER_LOCAL_HOST, port: int = SERVER_LOCAL_PORT, max_clients_count: None | int = None) -> None:
        super().__init__(host, port)
        try:
            self.net.bind((self.host, self.port))
        except:
            self.host = SERVER_LOCAL_HOST
            self.port = SERVER_LOCAL_PORT
            self.net.bind((self.host, self.port))
        debug.ServerCreateDebug(self.host, self.port, 'Infinity' if max_clients_count is None else max_clients_count)
        self.net.listen(1)
        self.connected_clients = []
        self.sended_data = []
        self.recv_data = {}
        self.timer = 0
        self.max_clients_count = max_clients_count

        # connect and disconnect events ---------
        self.event_connect = False              
        self.event_connect_data = None

        self.event_disconnect = False
        self.event_disconnect_data = None
        # connect and disconnect events ---------

        self.recv_ping = 0
        self.send_ping = 0
        

    def wait_connets(self):
        debug.ServerWaitedDebug()
        self.event_connect = False
        self.event_connect_data = None
        
        try:
            net, addr = self.net.accept()
            id = net.recv(1024).decode()
            if self.max_clients_count is None:
                net.setblocking(0)
                self.connected_clients.append([net, addr, 0, id])
                debug.ServerAcceptConnect(addr, id, len(self.connected_clients), self.max_clients_count)
                self.event_connect = True
                self.event_connect_data = [id, addr]
            else:
                if (len(self.connected_clients)+1<=self.max_clients_count):
                    net.setblocking(0)
                    self.connected_clients.append([net, addr, 0, id])
                    debug.ServerAcceptConnect(addr, id, len(self.connected_clients), self.max_clients_count)
                    self.event_connect = True
                    self.event_connect_data = [id, addr]
                else:
                    debug.ServerClientsMaxed(addr[0], addr[1], len(self.connected_clients), self.max_clients_count)
        except:
            ...
    
    
    def recv_all(self, bufsize: int = 2048):
        self.recv_data = {}
        start_time = time.time()
        for clients in self.connected_clients:
            try:
                clients[0].setblocking(0)
                data = clients[0].recv(bufsize).decode()
                
                if data:
                    clients[2] = 0
                    data = literal_eval(data)
                    self.recv_data[data[0]] = data[1]
            except: ...
        self.recv_ping = (time.time() - start_time) * 100

    def send_all(self):
        start_time = time.time()
        for clients in self.connected_clients:
            try:
                clients[0].send(str(self.sended_data).encode())
            except: ...
        self.send_ping = (time.time() - start_time) * 100

    def send_packet_all(self, packet, time_out = 1):
        for clients in self.connected_clients:
            try:
                clients[0].send(packet)
            except: ...
        tick(time_out)

    def send_packet_this_client(self, client, packet):
        client.send(packet)

    def check_clients(self):
        self.timer+=1
        if self.timer%50==0:
            for clients in self.connected_clients:
                try:
                    clients[0].send(''.encode())
                except:
                    clients[2] += 1
                    debug.ServerClientSleep(clients[1][0], clients[1][1], clients[2])

        self.event_disconnect = False
        self.event_disconnect_data = None

        for clients in self.connected_clients:
            if clients[2]==5:
                
                debug.ServerClientDisconected(clients[1][0], clients[1][1], len(self.connected_clients) - 1, self.max_clients_count)

                self.event_disconnect = True
                self.event_disconnect_data = [clients[3], clients[1]]
                del self.connected_clients[self.connected_clients.index(clients)]
                break
    
class Client(Net):
    def __init__(self, host: str = SERVER_LOCAL_HOST, port: int = SERVER_LOCAL_PORT, id: int | str | None = None) -> None:
        super().__init__(host, port)
        self.recv_data = {}
        self.sended_data = []
        self.id = random.randint(0, 999999999) if id is None else id

    def connect(self):
        try:
            self.net.connect((self.host, self.port))
        except:
            self.host = SERVER_LOCAL_HOST
            self.port = SERVER_LOCAL_PORT
            self.net.connect((self.host, self.port))
            
        self.net.send(str(self.id).encode())
        self.net.setblocking(1)
        debug.ClientConnectDebug(self.host, self.port)

    def reconnect(self):
        self.net.connect((self.host, self.port))
        self.net.send(str(self.id).encode())
        debug.ClientConnectDebug(self.host, self.port)

    def recv_all(self, bufsize: int = 2048):
        data_bytes = self.net.recv(bufsize)
        data = data_bytes.decode()
        try:
            
            data = literal_eval(data)
            for value in data:
                self.recv_data[value[0]] = value[1]
            
        except: ...

    def recv_packet(self, bufsize: int = 2048):
        data_bytes = self.net.recv(bufsize)
        data = data_bytes.decode()
        
            
        #data = literal_eval(data)
        return data

    def send_all(self):
        self.net.send(str([self.id ,self.sended_data]).encode())

    def get_data(self, name: str):
        try:
            return self.recv_data[name]
        except: 
            return None

        




