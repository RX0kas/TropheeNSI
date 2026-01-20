from OpenGL.GL import *
from PIL import Image
from math import ceil,sqrt
class Texture:
    def __init__(self,path:str):
        self.__path = path
        self.__opengl_id = self.__generer_texture(path) # id de la texture
    
    def __generer_texture(self,path:str):
        image = Image.open(path).convert("RGBA")
        width, height = image.size
        image_data = image.tobytes()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # parametre
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id
    
    def __getId(self): return self.__opengl_id
    def __getPath(self): return self.__path
    
    id = property(__getId)
    chemin = property(__getPath)
    
class TextureManager:
    atlas_id = -1
    taille_texture = 128
    
    def __init__(self):
        self.__textures_data:list[Image] = [] #type: ignore
    
    def __generer_atlas_texture(self,taille,data):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        # parametre
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,taille,taille,0,GL_RGBA,GL_UNSIGNED_BYTE,data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture_id
    
    def creer(self,path:str):
        """
        Ajoute les donnees de l'image à la liste des textures
        Args:
            path (str): Chemin de l'image
        """
        print(f"Chargement de {path}")
        image = Image.open(path).convert("RGBA")
        width, height = image.size
        assert width==TextureManager.taille_texture and height==TextureManager.taille_texture, f"Les images doivents être {TextureManager.taille_texture}x{TextureManager.taille_texture}"
        self.__textures_data.append(image.load())
        
    def generer_texture_atlas(self): # TODO: créé un rectangle (Rectangle Packing Algorithm)
        """
        Créé une grande texture carré qui contient toutes les autres
        """
        n = len(self.__textures_data)
        taille_coter = ceil(sqrt(n))
        taille_atlas = taille_coter*TextureManager.taille_texture
        print(f"Creation de l'atlas pour {n} images, carré de {taille_coter} textures de coté et {taille_atlas} pixels")
        atlas = Image.new("RGBA",(taille_atlas,taille_atlas),(0,0,0,0))
        atlas_data = atlas.load()
        for y in range(taille_atlas):
            for x in range(taille_atlas):
                atlas_data[x,y] = self.__textures_data[x//TextureManager.taille_texture][x%TextureManager.taille_texture,y%TextureManager.taille_texture] # TODO: finir la creation de l'atlas texture (spritesheet)
        
        atlas.save("test.png",format="PNG")


if __name__ == "__main__":
    t = TextureManager()
    t.creer("test2.png")
    t.creer("test1.png")
    t.creer("test2.png")
    t.creer("test1.png")
    t.generer_texture_atlas()