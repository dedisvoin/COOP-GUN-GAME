from src.constants import STANDART_WINDOW_SIZE, STANDART_WINDOW_TITLE, STANDART_WINDOW_VSYNC
from src.window import Window, WindowEvents, WindowFlags
from src.window import *


GLOBAL_ID = 0


class AppSubProcess:
    def __init__(self, function: callable, rendering: bool = False, tps: float | int = 1, id_or_name: str = None, *args, **kvargs) -> 'AppSubProcess':
        global GLOBAL_ID
        self.id_or_name = id_or_name
        if self.id_or_name == None:
            self.id_or_name = GLOBAL_ID
            GLOBAL_ID+=1
        self.rendering = rendering
        self.function = function
        self.kvargs = kvargs
        self.args = args
        self.tps = tps
        self.timer = 0
        

    def update(self, win_delta: float):
        self.tps = max(0, self.tps)
        self.win_delta = win_delta
        self.timer += win_delta
        self.start = False
        if self.timer>=self.tps:
            
            self.timer = 0
            self.start = True

    def run(self):
        if self.rendering:
            self.function(delta=self.win_delta, *self.args, **self.kvargs)
        else:
            if self.start:
                self.function(delta=self.win_delta, *self.args, **self.kvargs)
                self.start = False

    def __str__(self) -> str:
        return f'App_Sub_Process {self.id_or_name=} {self.rendering=} {self.tps=} {self.timer=} {self.start=}'


###################################################################################################################################################
#                                                                                                                                                 #
#                                                                                                                                                 #
#                                                         BASIC APLICATION CLASS                                                                  #
#                                                                                                                                                 #
#                                                                                                                                                 #
###################################################################################################################################################
class App(Window):
    def __init__(self, size: list[int] = STANDART_WINDOW_SIZE, title: str = STANDART_WINDOW_TITLE, 
                 events: WindowEvents = WindowEvents(), vsync: bool = STANDART_WINDOW_VSYNC, flags: WindowFlags = WindowFlags.RESIZE, render_fps: bool = True) -> Window:
        
        super().__init__(size, title, events, vsync, flags, _render_fps = render_fps)
        self.processes: tuple[AppSubProcess, ...] = []
        self.tps = 60
        self.open = True

    def get_process(self, id: str) -> AppSubProcess:
        for process in self.processes: 
            if process.id_or_name == id:
                return process
           
            
    def add_process(self, process, type, tps, id):
        self.processes.append(AppSubProcess(process, type, tps, id))
        

    def run(self, function_process: AppSubProcess | tuple[AppSubProcess, ...] = [], bg_color: tuple[int, int, int] = STANDART_WINDOW_BG_COLOR) -> None:
        
        if len(function_process)>0: self.processes = function_process
        
        while self.update(bg_color):
            delta = self.tps / (self.fps+1)
            
            for process in self.processes:
                process.update(delta)
            
            for process in self.processes:
                process.run()
            self.render_fps()
        
        
        
        
        
            
            

def AppProcess(app, rendered: bool, tps: int = 0, id: str | int = None):
    def creator(funct: callable):
        app.add_process(funct, rendered, tps, id)
    return creator
