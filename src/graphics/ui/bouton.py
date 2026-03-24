import glfw

from src.event.windowEvent import *
from src.graphics.ui.drawable import Drawable
from src.math.vectors import *

class Bouton(Drawable):
    def __init__(self,texture_path:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1),enable:bool=True):
        super().__init__(texture_path,pos,taille,rotation,couleur)
        self.__callback_fn:Callable[["Bouton"],None] = [] # type: ignore
        self.enable = enable
        self.__clicked = False

    def __is_in(self,coord:Vec2):
        return (self.position.x - self.taille.x / 2 < coord.x < self.position.x + self.taille.x / 2 and self.position.y - self.taille.y / 2 < coord.y < self.position.y + self.taille.y / 2)

    @SystemEvenement.ecouter_class_func("MousePressedEvent")
    def on_mouse_pressed(self, event: MousePressedEvent):
        if self.enable and not self.__clicked and event.action == glfw.PRESS and event.button == glfw.MOUSE_BUTTON_1:
            world_pos = super().screen_to_world(event.pos[0],event.pos[1])
            if self.__is_in(world_pos):
                self.__clicked = True
                for callback in self.__callback_fn: # type: ignore
                    callback[0](self,*callback[1],**callback[2])
        
        if event.action == glfw.RELEASE and event.button == glfw.MOUSE_BUTTON_1:
            self.__clicked = False

    def ajouter_callback(self,fn:Callable[["Bouton",Any],None],args:tuple|None=None,kargs:dict|None=None):
        if args is None:
            args = ()
        if kargs is None:
            kargs = {}
        self.__callback_fn.append([fn,args,kargs])