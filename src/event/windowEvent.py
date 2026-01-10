from src.event.event import *

@SystemEvenement.enregistrer_event
class MouseMovedEvent:
    def __init__(self,x, y):
        self.x = x
        self.y = y

@SystemEvenement.enregistrer_event
class MouseScrollEvent:
    def __init__(self,xoffset,yoffset):
        self.x = xoffset
        self.y = yoffset

@SystemEvenement.enregistrer_event
class MousePressedEvent:
    def __init__(self,button, action, mods):
        self.button = button
        self.action = action
        self.mods = mods

@SystemEvenement.enregistrer_event
class WindowResizeEvent:
    def __init__(self,width, height):
        self.width = width
        self.height = height

@SystemEvenement.enregistrer_event
class KeyPressedEvent:
    def __init__(self,key:int, scancode:int, action:int, mods:int):
        self.key = key
        self.scancode = scancode
        self.action = action
        self.mods = mods