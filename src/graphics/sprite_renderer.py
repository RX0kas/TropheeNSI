from ctypes import *
from OpenGL.GL import *
from src.graphics.shader import Shader
from src.math.matrices import *
from src.math.vectors import *
from src.graphics.sprite import *
from src.graphics.camera import Camera


class SpriteRenderer:
    NOMBRE_SPRITE_MAX = 64


    def __init__(self, shader: Shader,capacite:int=1024):
        self.__shader = shader
        from numpy import array,float32
        self.__instance_data = array([],dtype=float32)

        self.creer_opengl_obj()
        
    def creer_opengl_obj(self):
        taille_float = sizeof(c_float)

        import numpy as np # Obligatoire pour envoyer les données car les listes ne sont pas implementer: "Haven't implemented type-inference for lists yet"

        vertices = np.array([-0.5,-0.5,0.5, -0.5, 0.5, 0.5,-0.5, 0.5],dtype=np.float32)
        
        indices = np.array([0,1,2,2,3,0],dtype=np.uint32)

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
        glVertexAttribPointer(0        , 2    ,GL_FLOAT,GL_FALSE            ,4*taille_float,ctypes.c_void_p(0))

        # instance vbo
        self.__instanceVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER,self.__instanceVBO)
        uv_size = taille_float*4
        self.__taille_layout = Mat4.get_gpu_memory_size()+Mat3.get_gpu_memory_size()+uv_size
        glBufferData(GL_ARRAY_BUFFER,SpriteRenderer.NOMBRE_SPRITE_MAX*self.__taille_layout,self.__instance_data,GL_DYNAMIC_DRAW)
        decallage = 0
        # model Matrice
        for i in range(3):
            glEnableVertexAttribArray(1+i)
            glVertexAttribPointer(1+i,3,GL_FLOAT,GL_FALSE,self.__taille_layout,ctypes.c_void_p(i*3*4))
            glVertexAttribDivisor(1+i,1)
        decallage += Mat3.get_gpu_memory_size()

        # les 4 vecteurs uv
        glEnableVertexAttribArray(4)
        glVertexAttribPointer(4,taille_float,GL_FLOAT,GL_FALSE,self.__taille_layout,ctypes.c_void_p(decallage))
        glVertexAttribDivisor(4,1)
        decallage += sizeof(ctypes.c_float)

        glEnableVertexAttribArray(5)
        glVertexAttribPointer(5,taille_float,GL_FLOAT,GL_FALSE,self.__taille_layout,ctypes.c_void_p(decallage))
        glVertexAttribDivisor(5,1)
        decallage += sizeof(ctypes.c_float)

        glEnableVertexAttribArray(6)
        glVertexAttribPointer(6,taille_float,GL_FLOAT,GL_FALSE,self.__taille_layout,ctypes.c_void_p(decallage))
        glVertexAttribDivisor(6,1)
        decallage += sizeof(ctypes.c_float)

        glEnableVertexAttribArray(7)
        glVertexAttribPointer(7,taille_float,GL_FLOAT,GL_FALSE,self.__taille_layout,ctypes.c_void_p(decallage))
        glVertexAttribDivisor(7,1)
        decallage += sizeof(ctypes.c_float)



    def dessiner(self):
        self.__shader.use()
        glBindVertexArray(self.__vao)
        #                       mode        ,count,type           ,indices,instancecount
        glDrawElementsInstanced(GL_TRIANGLES,6    ,GL_UNSIGNED_INT,None   ,len(self.__instance_data))

    def envoyer(self,sprite:Sprite):
        uv = TextureManager.getUV(sprite.texture_id)
        import numpy as np
        np.append(self.__instance_data,[Mat3.model(sprite.rotation, sprite.position, sprite.taille).getData(),*[uv[i] for i in range(4)]])