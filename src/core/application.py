import os
from math import sin
import glfw
from OpenGL.GL import *
from PIL import Image

from src.core.window import Window
from src.graphics.camera import Camera
from src.graphics.shader import Shader
from src.graphics.sprite_renderer import SpriteRenderer
from src.graphics.sprite import Sprite
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

    def run(self):
        self.__fenetre.show()

        lastFrame = 0.0
        
        test_image = Sprite("prototype.png",pos=Vec2(-5,-5),taille=Vec2(10,10))
        time = 0
        
        while not self.__fenetre.devrait_fermer():
            glfw.poll_events()
            currentFrame = self.__fenetre.get_time()
            deltaTime = currentFrame - lastFrame
            lastFrame = currentFrame
            glClearColor(0.8, 0.8, 0.8, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.__main_shader.use()
            self.__main_shader.setInt("uTexture", 0)
            self.__main_shader.setMat4f("view_projection_matrix", self.__camera.get_view_projection_matrix())

            self.__sprite_renderer.render_sprite(test_image)

            glfw.swap_buffers(self.__fenetre.get_window())
            time += deltaTime

        self.__fenetre.supprimer()

    def stop(self):
        glfw.set_window_should_close(self.__fenetre.get_window(), True)