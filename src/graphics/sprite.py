from src.math.vectors import *
from src.graphics.texture import TextureManager

class Sprite:
    """
    N'importe quel objet pouvant etre dessiner sur l'écran
    """
    def __init__(self,texturePath:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(10,10),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        self.texture_id = TextureManager.creer(texturePath)
        self.position = pos
        self.taille = taille
        self.rotation = rotation
        self.couleur = couleur
        self.va = None
    