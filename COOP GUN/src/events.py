from src.keyboard import *
from src.mouse import *

class Event:
    class Types:
        MOUSE_PRESS = 'MOUSE_PRESS'
        MOUSE_CLICK = 'MOUSE_CLICK'
        KEY_PRESS = 'KEY_PRESS'
        KEY_CLICK = 'KEY_CLICK'

    def __init__(self, type: Types, id: int | str) -> None:
        self.__key = None
        self.__btn = None

        self.__mouse = None
        self.__keyboard = None

        self.__type = type
        self.__togled = False
        self.__id = id
        

    def key(self, key: Key):
        self.__key = key
        self.__keyboard = Keyboard()
        return self
    
    def btn(self, btn: Mouse.Button):
        self.__btn = btn
        self.__mouse = Mouse()
        return self
    
    def get_btn(self):
        return self.__btn
    
    def get_key(self):
        return self.__key
    
    @property
    def type(self): return self.__type

    @property
    def mouse(self): return self.__mouse

    @property
    def keyboard(self): return self.__keyboard

    @property
    def togled(self):
        return self.__togled
    
    @togled.setter
    def togled(self, togled: bool):
        self.__togled = togled

    @property
    def id(self): return self.__id
    
    
class EventLoop:
    def __init__(self) -> None:
        self.__events: list[Event] = []

    def add(self, event: Event):
        self.__events.append(event)

    def get_event(self, id: int | str) -> Event:
        for event in self.__events:
            if event.id == id: return event

    def get(self, id: int | str) -> bool:
        for event in self.__events:
            if event.id == id: return event.togled

    def update(self):
        for event in self.__events:
            if event.type == Event.Types.MOUSE_PRESS:
                event.togled = event.mouse.press(event.get_btn())
            if event.type == Event.Types.MOUSE_CLICK:
                event.togled = event.mouse.click(event.get_btn())
            if event.type == Event.Types.KEY_PRESS:
                event.togled = event.keyboard.press(event.get_key())
            if event.type == Event.Types.KEY_CLICK:
                event.togled = event.keyboard.click(event.get_key())


