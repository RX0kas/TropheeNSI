from OpenGL.GL import *
from PIL import Image
from math import ceil,sqrt
from dataclasses import dataclass

@dataclass(frozen=True) # dit que c'est une class qui contient que des attributs qui ne peuvent pas etre modifier
class UV:
    """
    Coordonnées dans la texture
    """
    u0:float
    v0:float
    u1:float
    v1:float

    def __getitem__(self,i):
        if i==0: return self.u0
        if i==1: return self.v0
        if i==2: return self.u1
        if i==3: return self.v1
        raise IndexError(f"UV[{i}] n'est pas autoriser")


class TextureManager:
    atlas_id = -1
    taille_texture = 128
    __textures_data:list[Image.Image] = []
    __uvs:list[UV] = []
    __cache = {} # __cache[path] = index in __textures_data

    @classmethod
    def __generer_atlas_texture(cls,image:Image.Image) -> int:
        data = image.tobytes()
        largeur, hauteur = image.size
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # parametre
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAX_ANISOTROPY, 16.0)

        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,largeur,hauteur,0,GL_RGBA,GL_UNSIGNED_BYTE,data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return texture_id
    
    @classmethod
    def creer(cls,path:str) -> int:
        """
        Ajoute les donnees de l'image à la liste des textures
        Args:
            path (str): Chemin de l'image
        """
        if path in cls.__cache:
            return cls.__cache[path]

        print(f"Chargement de {path}")
        image = Image.open(path).convert("RGBA")
        width, height = image.size
        cls.__textures_data.append(image.copy())
        id_texture = len(cls.__textures_data)-1
        cls.__cache[path] = id_texture
        return id_texture
    
    @classmethod
    def __calculer_taille_atlas(cls) -> int:
        aire_totale = sum(img.width*img.height for img in cls.__textures_data)
        taille = ceil(sqrt(aire_totale)*1.2)
        puissance = 1
        while puissance < taille:
            puissance *= 2
        return puissance
        
    @classmethod
    def generer_texture_atlas(cls):
        """
        Créé une grande texture carré qui contient toutes les autres
        """
        n = len(cls.__textures_data)
        taille_atlas = cls.__calculer_taille_atlas()
        print(f"Creation de l'atlas pour {n} images, {taille_atlas}x{taille_atlas} pixels")
        atlas = Image.new("RGBA",(taille_atlas,taille_atlas),(0,0,0,0))
        curseur_x = 0
        curseur_y = 0
        hauteur_etagere = 0
        for img in cls.__textures_data:
            w, h = img.size
            if curseur_x + w >taille_atlas:
                curseur_x = 0
                curseur_y += hauteur_etagere
                hauteur_etagere = 0
            
            atlas.paste(img,(curseur_x,curseur_y))
            
            u0 = curseur_x / taille_atlas
            v0 = curseur_y / taille_atlas
            u1 = (curseur_x + w)/ taille_atlas
            v1 = (curseur_y + h)/ taille_atlas
            cls.__uvs.append(UV(u0,v0,u1,v1))
            curseur_x += w
            hauteur_etagere = max(hauteur_etagere,h)
            
        
        atlas.save("test.png",format="PNG")
        cls.atlas_id = cls.__generer_atlas_texture(atlas)
    
    
    
    @classmethod
    def getUV(cls,index) -> UV:
        return cls.__uvs[index]