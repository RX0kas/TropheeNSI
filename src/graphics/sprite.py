from src.math.vectors import *
from src.graphics.texture import TextureManager
class Sprite:
    def __init__(self,texture:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        self.texture_id = TextureManager.creer(texture)
        self.position = pos
        self.taille = taille
        self.rotation = rotation
        self.couleur = couleur
        self.va = None
    