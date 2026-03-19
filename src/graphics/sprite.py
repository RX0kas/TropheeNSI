from src.math.vectors import *
from src.graphics.texture import TextureManager

class Sprite:
    """
    N'importe quel objet pouvant etre dessiner sur l'écran
    """
    def __init__(self,texturePath:str,pos:Vec2=Vec2(0,0),taille:Vec2=Vec2(10,10),rotation:float=0,couleur:Vec3=Vec3(1,1,1)):
        self.texture_id = TextureManager.creer(texturePath)
        self.position = pos
        if isinstance(taille,int) or isinstance(taille,float):
            self.__taille:Vec2 = Vec2(taille,taille)
        else:
            self.__taille:Vec2 = taille
        self.rotation = rotation
        self.couleur = couleur
        self.va = None
    
    @property
    def taille(self):
        return self.__taille

    @taille.setter
    def taille(self, v:Vec2|int|float):
        if isinstance(v,int) or isinstance(v,float):
            self.__taille:Vec2 = Vec2(v,v)
        else:
            self.__taille:Vec2 = v