import os

import glfw
from OpenGL.GL import *
from PIL import Image

from src.core.window import Window
from src.graphics.camera import Camera
from src.graphics.shader import Shader
from src.graphics.sprite_renderer import SpriteRenderer
from src.math.vectors import Vec2


class Application:
    VERSION = "0.0.1"

    def __init__(self):
        self.__fenetre = Window(800, 600, "Trophe NSI - " + Application.VERSION)
        from OpenGL.GL import glGetString, GL_VERSION
        try:
            print("PyOpenGL GL_VERSION:", glGetString(GL_VERSION))
            print("GLSL VERSION:", glGetString(GL_SHADING_LANGUAGE_VERSION))

        except Exception as e:
            print("PyOpenGL can't query GL_VERSION yet:", e)

        self.__main_shader = Shader(open(os.path.join("shaders","main.vert")).read(),open(os.path.join("shaders","main.frag")).read())

        self.__camera = Camera()
        self.__sprite_renderer = SpriteRenderer(self.__main_shader)

    def generer_texture(self):
        image = Image.open("prototype.png").convert("RGBA")
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


    def run(self):

        texture = self.generer_texture()
        self.__fenetre.show()

        lastFrame = 0.0
        while not self.__fenetre.devrait_fermer():
            glfw.poll_events()
            currentFrame = self.__fenetre.get_time()
            deltaTime = currentFrame - lastFrame
            lastFrame = currentFrame
            glClearColor(1, 1, 1, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.__main_shader.use()
            self.__main_shader.setInt("uTexture", 0)
            self.__main_shader.setMat4f("view_projection_matrix", self.__camera.get_view_projection_matrix())

            self.__sprite_renderer.render_sprite(texture, Vec2(-5, -5), Vec2(10, 10), 0, [1, 1, 1])

            glfw.swap_buffers(self.__fenetre.get_window())

        self.__fenetre.supprimer()

    def stop(self):
        glfw.set_window_should_close(self.__fenetre.get_window(), True)