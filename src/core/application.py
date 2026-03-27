import os
import glfw
from OpenGL.GL import *

from src.core.window import Window
from src.debug.debug_box import DebugDraw
from src.graphics.camera import Camera
from src.graphics.shader import Shader
from src.graphics.sprite_renderer import SpriteRenderer
from src.graphics.ui.bouton import Bouton
from src.math.vectors import Vec2
from src.graphics.texture import TextureManager
from src.graphics.text.Text import Texte
from src.graphics.ui.ui_manager import UIManager
from src.game.gameManager import GameManager

#from os.path import join
#
#def afficher(button:Bouton,*args,**kargs):
#    print(f"args: {args},kargs:{kargs}")

class Application:
    __instance = None

    def __init__(self):
        if Application.__instance is None:
            Application.__instance = self
        else:
            print("Une Application existe déja")
            exit(1)
        self.__fenetre = Window(800, 600, "Trophe NSI - BlackJack")
        from OpenGL.GL import glGetString, GL_VERSION
        try:
            print("PyOpenGL GL_VERSION:", glGetString(GL_VERSION))
            print("GLSL VERSION:", glGetString(GL_SHADING_LANGUAGE_VERSION))

        except Exception as e:
            print("PyOpenGL can't query GL_VERSION yet:", e)

        self.__main_shader = Shader("""
#version 330 core

layout (location = 0) in vec2 aPos;     // position du triangle de base
layout (location = 1) in vec2 iPos;     // position de l'instance
layout (location = 2) in vec2 iScale;
layout (location = 3) in float iRot;
layout (location = 4) in vec4 iUV;      // u0 v0 u1 v1

uniform mat4 view_projection_matrix;

out vec2 TexCoords;

vec2 rotate(vec2 v, float a) {
    float c = cos(a);
    float s = sin(a);
    return vec2(
        c * v.x - s * v.y,
        s * v.x + c * v.y
    );
}

void main() {
    vec2 local = aPos * iScale;
    vec2 coordMonde = rotate(local, iRot) + iPos;
    vec3 p = (view_projection_matrix * vec4(coordMonde, 0.0, 1.0)).xyz;
    gl_Position = vec4(p,1.0);

    vec2 uvLocal = aPos + vec2(0.5);
    TexCoords = mix(iUV.xy, iUV.zw, uvLocal);
}
""","""
#version 330 core

in vec2 TexCoords;
out vec4 FragColor;

uniform sampler2D uTexture;

void main() {
    FragColor = texture(uTexture, TexCoords);
}
""")

        self.__camera = Camera()
        self.__sprite_renderer = SpriteRenderer(self.__main_shader)
        Texte.loadCharacters()
        self.__game_manager = GameManager()

        UIManager.load_cards()

    def run(self):
        self.__fenetre.show()
        lastFrame = 0.0
        time = 0
    
        self.__game_manager.setup()
        TextureManager.generer_texture_atlas()
        DebugDraw.load()

        #b = Bouton(join("assets","card_spades_Q.png"),taille=Vec2(10,10))
        #b.ajouter_callback(afficher,(5,52,1),{"a":2}) # type: ignore

        while not self.__fenetre.devrait_fermer():
            # preparation
            glfw.poll_events()
            currentFrame = self.__fenetre.get_time()
            deltaTime = currentFrame - lastFrame
            lastFrame = currentFrame

            # Updating
            self.__game_manager.update()

            # Rendering
            glClearColor(0.8, 0.8, 0.8, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.__main_shader.use()
            self.__main_shader.setMat4f("view_projection_matrix", self.__camera.get_view_projection_matrix())
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, TextureManager.atlas_id)
            self.__main_shader.setInt("uTexture", 0)
            
            UIManager.draw_ui()


            self.__sprite_renderer.dessiner()
            self.__sprite_renderer.nettoyer()

            Bouton.draw_debug()
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