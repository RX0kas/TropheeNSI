from src.math.vectors import *

class Sprite:
    def __init__(self,texture,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(1,1),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        self.texture = texture
        self.position = pos
        self.taille = taille
        self.rotation = rotation
        self.couleur = couleur
    
    