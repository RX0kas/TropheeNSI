import os
import glfw
from OpenGL.GL import *

from src.core.window import Window
from src.graphics.camera import Camera
from src.graphics.shader import Shader
from src.graphics.sprite_renderer import SpriteRenderer
from src.graphics.ui.bouton import Bouton
from src.math.vectors import Vec2
from src.graphics.texture import TextureManager
from src.graphics.text.Text import Characters
from src.graphics.ui.ui_manager import UIManager
from src.game.gameManager import GameManager

class Application:
    __instance = None

    def __init__(self):
        if Application.__instance is None:
            Application.__instance = self
        else:
            print("Une Application existe déja")
            exit(1)
        self.__fenetre = Window(800, 600, "Trophe NSI")
        from OpenGL.GL import glGetString, GL_VERSION
        try:
            print("PyOpenGL GL_VERSION:", glGetString(GL_VERSION))
            print("GLSL VERSION:", glGetString(GL_SHADING_LANGUAGE_VERSION))

        except Exception as e:
            print("PyOpenGL can't query GL_VERSION yet:", e)

        self.__main_shader = Shader(open(os.path.join("shaders","main.vert")).read(),open(os.path.join("shaders","main.frag")).read())
        self.__text_shader = Shader(open(os.path.join("shaders","text.vert")).read(),open(os.path.join("shaders","text.frag")).read())

        self.__camera = Camera()
        self.__sprite_renderer = SpriteRenderer(self.__main_shader)
        Characters.loadCharacters()
        UIManager.load_cards()
        
        self.__game_manager = GameManager()

    def run(self):
        self.__fenetre.show()
        lastFrame = 0.0
        time = 0
    
        self.__game_manager.setup()
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

            self.__sprite_renderer.dessiner()
            self.__sprite_renderer.nettoyer()
            
            
            self.__text_shader.setMat4f("projection", self.__camera.get_view_projection_matrix())
            
            
            UIManager.draw_cards()


            self.__sprite_renderer.dessiner()
            self.__sprite_renderer.nettoyer()
            glfw.swap_buffers(self.__fenetre.get_window())
            time += deltaTime

        self.__fenetre.supprimer()

    def stop(self):
        glfw.set_window_should_close(self.__fenetre.get_window(), True)

    def get_window(self):
        return self.__fenetre
    
    def get_camera(self):
        return self.__camera
    
    def get_sprite_renderer(self):
        return self.__sprite_renderer
    
    def get_game_manager(self):
        return self.__game_manager

    @classmethod
    def get_instance(cls) -> "Application":
        return cls.__instance # type: ignore