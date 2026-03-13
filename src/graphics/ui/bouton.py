import glfw

from src.event.windowEvent import *
from src.graphics.ui.drawable import Drawable
from src.math.vectors import *

class Bouton(Drawable):
    def __init__(self,texture_path:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        super().__init__(texture_path,pos,taille,rotation,couleur)
        self.__callback_fn:Callable[["Bouton"],None] = [] # type: ignore

    def __is_in(self,coord:Vec2):
        return (self.position.x - self.taille.x / 2 < coord.x < self.position.x + self.taille.x / 2 and self.position.y - self.taille.y / 2 < coord.y < self.position.y + self.taille.y / 2)

    @SystemEvenement.ecouter_class_func("MousePressedEvent")
    def on_mouse_pressed(self, event: MousePressedEvent):
        if self.__is_in(Drawable.screen_to_pourcentage(event.pos[0],event.pos[1])) and event.action == glfw.PRESS and event.button == glfw.MOUSE_BUTTON_1:
            for callback in self.__callback_fn: # type: ignore
                callback(self)

    def ajouter_callback(self,fn:Callable[["Bouton"],None]):
        self.__callback_fn.append(fn)