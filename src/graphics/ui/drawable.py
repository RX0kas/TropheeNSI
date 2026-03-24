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

    @staticmethod
    def screen_to_pourcentage(x,y):
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

        newX = left + (x / w) * (right - left)
        newY = top - (y / h) * (top - bottom)
        return Vec2(newX,newY)

    @staticmethod
    def screen_to_world(x,y) -> Vec2:
        from src.core.application import Application
        app = Application.get_instance()
        window = app.get_window()
        camera = app.get_camera()
        
        ndc_x = (x/window.get_width()) * 2.0 - 1.0
        ndc_y = 1.0 - (y / window.get_height()) * 2.0
        
        vp_inv = camera.get_view_projection_matrix().inverse()
        world = vp_inv * Vec4(ndc_x,ndc_y,0.0,1.0)
        return Vec2(world.x,world.y)