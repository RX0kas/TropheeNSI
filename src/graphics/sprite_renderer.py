from OpenGL.GL import *
from src.graphics.shader import Shader
from src.graphics.sprite import *

# Obligatoire pour envoyer les données car les listes ne sont pas implementer: "Haven't implemented type-inference for lists yet"
from numpy import array,float32,uint32

class SpriteRenderer:
    NOMBRE_SPRITE_MAX = 1024


    def __init__(self, shader: Shader,capacite:int=1024):
        self.__shader = shader
        self.__instance_data = []
        self.__instance_data_np = array(self.__instance_data,dtype=float32)

        self.creer_opengl_obj()
        
    def creer_opengl_obj(self):
        taille_float = sizeof(c_float)

        vertices = array([-0.5,-0.5,0.5, -0.5, 0.5, 0.5,-0.5, 0.5],dtype=float32)
        
        indices = array([0,1,2,2,3,0],dtype=uint32)

        self.__vao = glGenVertexArrays(1)
        glBindVertexArray(self.__vao)


        # Sprite Vertex buffer object (vbo)
        self.__vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.__vbo)
        glBufferData(GL_ARRAY_BUFFER,vertices.nbytes,vertices,GL_STATIC_DRAW)
        
        # indices
        self.__ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,self.__ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,indices.nbytes,indices,GL_STATIC_DRAW)

        # position
        glEnableVertexAttribArray(0)
        #                     index,    taille,type,    doit etre normaliser, stride          , pointer vide
        glVertexAttribPointer(0        , 2    ,GL_FLOAT,GL_FALSE            ,2*taille_float,ctypes.c_void_p(0))

        # instance vbo
        self.__instanceVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.__instanceVBO)

        self.__taille_layout = 2 * taille_float + 2 * taille_float + 1 * taille_float + 4 * taille_float

        glBufferData(GL_ARRAY_BUFFER,SpriteRenderer.NOMBRE_SPRITE_MAX*self.__taille_layout,self.__instance_data_np,GL_DYNAMIC_DRAW)
        decallage = 0
        
        # iPos
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.__taille_layout, ctypes.c_void_p(decallage))
        glVertexAttribDivisor(1, 1)
        decallage += 2 * taille_float

        # iScale
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.__taille_layout, ctypes.c_void_p(decallage))
        glVertexAttribDivisor(2, 1)
        decallage += 2 * taille_float

        # iRot
        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 1, GL_FLOAT, GL_FALSE, self.__taille_layout, ctypes.c_void_p(decallage))
        glVertexAttribDivisor(3, 1)
        decallage += taille_float

        # iUV (vec4)
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4, 4, GL_FLOAT, GL_FALSE, self.__taille_layout, ctypes.c_void_p(decallage))
        glVertexAttribDivisor(4, 1)

    def dessiner(self):
        if len(self.__instance_data) == 0:
            return

        self.__shader.use()
        glBindBuffer(GL_ARRAY_BUFFER, self.__instanceVBO)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.__instance_data_np.nbytes, self.__instance_data_np)
        glBindVertexArray(self.__vao)

        nombre_sprites = len(self.__instance_data)
        glDrawElementsInstanced(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None, nombre_sprites)

    def envoyer(self, sprite: Sprite):
        if len(self.__instance_data) >= SpriteRenderer.NOMBRE_SPRITE_MAX:
            print("Trop de sprite doivent etre dessiner")
            return
        uv = TextureManager.getUV(sprite.texture_id)

        self.__instance_data.append([
            sprite.position.x, sprite.position.y,
            sprite.taille.x, sprite.taille.y,
            sprite.rotation,
            uv.u0, uv.v1,
            uv.u1, uv.v0
        ])
        self.__instance_data_np = array(self.__instance_data,dtype=float32)

    def nettoyer(self):
        self.__instance_data.clear()
        self.__instance_data_np = array(self.__instance_data,dtype=float32)