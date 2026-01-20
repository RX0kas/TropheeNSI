from OpenGL.GL import *
from PIL import Image

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