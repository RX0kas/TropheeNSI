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
from src.graphics.ui.bouton import Bouton
from src.math.vectors import Vec2
from src.graphics.texture import TextureManager


class Application:
    VERSION = "0.1.0"
    __instance = None

    def __init__(self):
        if Application.__instance is None:
            Application.__instance = self
        else:
            print("Une Application existe déja")
            exit(1)
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

        #images = [Sprite("cat2.png" if x%2==0 else "cat.png",pos=Vec2(x*15,y*15),taille=Vec2(10,10),rotation=x+y) for x in range(-10,10) for y in range(-10,10)]
        time = 0

        button = Bouton("cat.png",pos=Vec2(0,0),taille=Vec2(20,20))

        def exempleCallback(button:Bouton):
            print("Button pressed")

        button.ajouter_callback(exempleCallback)


        TextureManager.generer_texture_atlas()
        while not self.__fenetre.devrait_fermer():
            # preparation
            glfw.poll_events()
            currentFrame = self.__fenetre.get_time()
            deltaTime = currentFrame - lastFrame
            lastFrame = currentFrame
            glClearColor(0.8, 0.8, 0.8, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.__main_shader.use()
            self.__main_shader.setMat4f("view_projection_matrix", self.__camera.get_view_projection_matrix())
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, TextureManager.atlas_id)
            self.__main_shader.setInt("uTexture", 0)
            # dit quoi afficher
            #for i in images:
            #    self.__sprite_renderer.envoyer(i)
            self.__sprite_renderer.envoyer(button)

            self.__sprite_renderer.dessiner()
            self.__sprite_renderer.nettoyer()
            glfw.swap_buffers(self.__fenetre.get_window())
            time += deltaTime

        self.__fenetre.supprimer()

    def stop(self):
        glfw.set_window_should_close(self.__fenetre.get_window(), True)

    def get_window(self):
        return self.__fenetre

    @classmethod
    def get_instance(cls) -> "Application":
        return cls.__instance # type: ignore