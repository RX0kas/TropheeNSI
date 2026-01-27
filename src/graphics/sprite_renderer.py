from OpenGL.GL import *
from src.graphics.shader import Shader
from src.math.matrices import *
from src.math.vectors import *
from src.graphics.sprite import *
from src.graphics.camera import Camera
class SpriteRenderer:
    def __init__(self, shader: Shader,capacite:int=1024):
        self.shader = shader
        """self.shader = shader
        self.__nombre_vertex = 0
        self.__capacite_vertex = capacite
        self.__vertex = []
        self.sprite_vertices = [
            0.0, 1.0,  0.0, 1.0,
            1.0, 0.0,  1.0, 0.0,
            0.0, 0.0,  0.0, 0.0,

            0.0, 1.0,  0.0, 1.0,
            1.0, 1.0,  1.0, 1.0,
            1.0, 0.0,  1.0, 0.0
        ]

        # creation objet opengl
        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer_object = glGenBuffers(1)

        # initialisation vertex array
        glBindVertexArray(self.vertex_array)

        # initialisation vertex buffer object
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_object)
        taille_memoire_alouer = (len(self.sprite_vertices) * sizeof(GLfloat))*self.__capacite_vertex
        print(f"Allocution de {taille_memoire_alouer}o pour le vbo")
        glBufferData(GL_ARRAY_BUFFER,taille_memoire_alouer,GL_NONE,GL_STATIC_DRAW)

        stride = 4 * sizeof(GLfloat)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(0))

        # Texture coords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(2 * sizeof(GLfloat)))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)"""

    @classmethod
    def creer_vertex_array(cls,uv,x,y) -> int:
        w = Camera.taille_fenetre
        h = Camera.taille_fenetre
        vertices = [
            x,y,        uv.u0,uv.v1,
            x+w,y,      uv.u1,uv.v1,
            x+w,y+h,    uv.u1,uv.v0,
            x,y,        uv.u0,uv.v1,
            x+w,y+h,    uv.u1,uv.v0,
            x,y+h,      uv.u0,uv.v0
        ]
               
        # creation objet opengl
        vertex_buffer_object = glGenBuffers(1)
        vertex_array = glGenVertexArrays(1)
        
        # initialisation vertex buffer object
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
        glBindVertexArray(vertex_array)
        
        glBufferData(GL_ARRAY_BUFFER,len(vertices) * sizeof(GLfloat),(GLfloat * len(vertices))(*vertices),GL_STATIC_DRAW)
        stride = 4 * sizeof(GLfloat)
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(0))
        # texture coords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(2 * sizeof(GLfloat)))

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        return vertex_array
    
    def dessiner(self):
        pass

    def envoyer(self,sprite:Sprite):
        """# TODO: utiliser le model matrice
        if self.__nombre_vertex>=self.__capacite_vertex:
            self.dessiner()"""
        pass
        
        
    def render_sprite(self,sprite:Sprite):
        if sprite.va is None:
            sprite.va = self.creer_vertex_array(TextureManager.getUV(sprite.texture_id),sprite.position.x,sprite.position.y)
        
        self.shader.use()
        model_matrix = Mat3.model(sprite.rotation,sprite.position,sprite.taille)

        self.shader.setMat3f("model_matrix",model_matrix)
        self.shader.setVec3f("couleur",sprite.couleur)

        glBindVertexArray(sprite.va)
        glDrawArrays(GL_TRIANGLES,0,6)
        glBindVertexArray(0)