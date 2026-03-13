from src.event.windowEvent import *
from src.graphics.ui.drawable import Drawable
from src.math.vectors import *

class Bouton(Drawable):
    def __init__(self,texture_path:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        super().__init__(texture_path,pos,taille,rotation,couleur)
        self.__callback_fn:Callable[["Bouton"],None] = [] # type: ignore

    @SystemEvenement.ecouter_class_func("MouseMovedEvent")
    def on_mouse_move(self, event: MouseMovedEvent):
        from src.core.application import Application
        from src.graphics.camera import Camera
        window = Application.get_instance().get_window()
        w = window.get_width()
        h = window.get_height()

        aspect = window.get_aspect()

        hauteur = Camera.taille_fenetre / Camera.zoom
        largeur = hauteur * aspect

        left = -largeur / 2
        right = largeur / 2
        bottom = -hauteur / 2
        top = hauteur / 2

        x = left + (event.x / w) * (right - left)
        y = top - (event.y / h) * (top - bottom)

        if (self.position.x - self.taille.x / 2 < x < self.position.x + self.taille.x / 2 and
                self.position.y - self.taille.y / 2 < y < self.position.y + self.taille.y / 2):
            for callback in self.__callback_fn: # type: ignore
                callback(self)
            
    def ajouter_callback(self,fn:Callable[["Bouton"],None]):
        self.__callback_fn.append(fn)