from src.graphics.text.characterSlot import CharacterSlot
from OpenGL.GL import *
import freetype
from numpy import asarray,float32

from src.math.vectors import *
from src.math.matrices import Mat4
from src.graphics.shader import Shader

import os

class Texte:
    FichierPolice = "OpenSans-Medium.ttf"
    __chars = dict()
    __loaded = False
    __shader:Shader|None = None
  
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
        
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        
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
        cls.__loaded = True
    
        cls.__shader = Shader(open(os.path.join("shaders","text.vert")).read(),open(os.path.join("shaders","text.frag")).read())
    @staticmethod
    def __ortho(left,right,bottom,top) -> Mat4:
        m =  Mat4()
        m[0,0] = 2/(right-left)
        m[1,1] = 2/(top-bottom)
        m[0,2] = -(right+left)/(right-left)
        m[1,2] = -(top+bottom)/(top-bottom)
        m[3,3] = 1
        return m

    @classmethod
    def render_text(cls,text,x,y,scale:float|int|Vec2|Vec3,color):
        assert(cls.__shader is not None)
        from src.core.application import Application
        cls.__shader.use()
        cls.__shader.setVec3f("textColor",color)
        cls.__shader.setInt("text",0)
        cls.__shader.setMat4f("view_projection_matrix", cls.__ortho(0,Application.get_instance().get_window().get_width(),Application.get_instance().get_window().get_height(),0))
        #cls.__shader.setMat4f("view_projection_matrix", Application.get_instance().get_camera().get_view_projection_matrix())

        cls.__shader.setFloat("uAspect",Application.get_instance().get_window().get_aspect())
        blend_enable = glIsEnabled(GL_BLEND)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glActiveTexture(GL_TEXTURE0)

        glBindVertexArray(cls.__VAO)
        # Pour chaque charactere
        for c in text:
            ch = cls.__chars[c]
            w, h = ch.textureSize
            xpos = 0
            ypos = 0
            if isinstance(scale,int) or isinstance(scale,float):
                w = w*scale
                h = h*scale
                xpos = x + ch.bearing[0] * scale
                ypos = y - (h - ch.bearing[1] * scale)
            elif isinstance(scale,Vec2) or isinstance(scale,Vec3):
                w = scale.x
                h = scale.y
                xpos = x + ch.bearing[0] * scale.x
                ypos = y - (h - ch.bearing[1] * scale.y)
            
            
            
            vertices = cls.__get_rendering_buffer(xpos,ypos,w,h)

            # On le dessine
            glBindTexture(GL_TEXTURE_2D, ch.texture)
            glBindBuffer(GL_ARRAY_BUFFER, cls.__VBO)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)

            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glDrawArrays(GL_TRIANGLES, 0, 6)
            
            # On avance le curseur
            if isinstance(scale,int) or isinstance(scale,float):
                x += (ch.advance >> 6) * scale
            elif isinstance(scale,Vec2) or isinstance(scale,Vec3):
                x += (ch.advance >> 6) * scale.x
        
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D,0)
        glUseProgram(0)
        if not blend_enable:
            glDisable(GL_BLEND)
        glPixelStorei(GL_UNPACK_ALIGNMENT,4)
