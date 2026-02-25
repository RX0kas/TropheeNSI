from src.event.windowEvent import *
from src.graphics.sprite import Sprite
from src.math.vectors import *


class Drawable(Sprite):
    """
    Representes les éléments d'interface
    Séparé de Sprite pour que ce soit plus simple de les gerer
    """
    def __init__(self,texture_path:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        super().__init__(texture_path,pos,taille,rotation,couleur)
        SystemEvenement.enregistrer_event_class(self)

    @SystemEvenement.ecouter_class_func("MouseMovedEvent")
    def on_mouse_move(self,event:MouseMovedEvent):
        pass

    @SystemEvenement.ecouter_class_func("MouseScrollEvent")
    def on_mouse_scroll(self, event: MouseScrollEvent):
        pass

    @SystemEvenement.ecouter_class_func("MousePressedEvent")
    def on_mouse_pressed(self,event:MousePressedEvent):
        pass