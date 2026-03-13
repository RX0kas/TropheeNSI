from src.graphics.text.characterSlot import CharacterSlot
from OpenGL.GL import *
import freetype
from numpy import asarray,float32

from src.math.vectors import Vec3


class Characters:
    FichierPolice = "OpenSans-Medium.ttf"
    __chars = dict()
    __loaded = False
    
    @staticmethod
    def __get_rendering_buffer(xpos, ypos, w, h, zfix=0.0):
        return asarray([
            xpos,     ypos - h, 0, 0,
            xpos,     ypos,     0, 1,
            xpos + w, ypos,     1, 1,
            xpos,     ypos - h, 0, 0,
            xpos + w, ypos,     1, 1,
            xpos + w, ypos - h, 1, 0
        ], float32)
    
    @classmethod
    def loadCharacters(cls):
        if cls.__loaded:
            print("Les characters sont déja charger")
            return
        
        face = freetype.Face(cls.FichierPolice)
        face.set_char_size(48*64)
        
        for i in range(0,128):
            face.load_char(chr(i))
            glyph = face.glyph

            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0, GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            cls.__chars[chr(i)] = CharacterSlot(texture,glyph)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
        # Opengl Object
        cls.__VAO = glGenVertexArrays(1)
        glBindVertexArray(cls.__VAO)

        cls.__VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, cls.__VBO)
        glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    @classmethod
    def render_text(cls,shaderProgram,text,x,y,scale,color):
        face = freetype.Face(cls.FichierPolice)
        face.set_char_size(48*64)
        shaderProgram.use()
        shaderProgram.setVec3f("textColor",Vec3(color[0]/255,color[1]/255,color[2]/255))

        glActiveTexture(GL_TEXTURE0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindVertexArray(cls.__VAO)
        # Pour chaque charactere
        for c in text:
            ch = cls.__chars[c]
            w, h = ch.textureSize
            w = w*scale
            h = h*scale
            vertices = cls.__get_rendering_buffer(x,y,w,h)

            # On le dessine
            glBindTexture(GL_TEXTURE_2D, ch.texture)
            glBindBuffer(GL_ARRAY_BUFFER, cls.__VBO)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glDrawArrays(GL_TRIANGLES, 0, 6)
            
            # On avance le curseur
            x += (ch.advance>>6)*scale
