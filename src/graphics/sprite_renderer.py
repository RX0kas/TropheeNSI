from OpenGL.GL import *
from src.graphics.shader import Shader
from src.math.matrices import *
from src.math.vectors import Vec2

class SpriteRenderer:
    def __init__(self, shader: Shader):
        self.shader = shader

        vertices = [
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
        glBufferData(GL_ARRAY_BUFFER,len(vertices) * sizeof(GLfloat),(GLfloat * len(vertices))(*vertices),GL_STATIC_DRAW)

        stride = 4 * sizeof(GLfloat)

        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(0))

        # Texture coords
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1,2,GL_FLOAT,GL_FALSE,stride,ctypes.c_void_p(2 * sizeof(GLfloat)))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)



    def render_sprite(self,texture,position:Vec2,taille:Vec2,rotation:float,couleur):
        self.shader.use()
        model_matrix = Mat3.model(rotation,position,taille)

        self.shader.setMat3f("model_matrix",model_matrix)
        self.shader.setVec3f("couleur",couleur[0],couleur[1],couleur[2])

        # envoie de la texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D,texture)

        glBindVertexArray(self.vertex_array)
        glDrawArrays(GL_TRIANGLES,0,6)
        glBindVertexArray(0)