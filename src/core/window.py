from glfw import *
from OpenGL.GL import *
from src.event.windowEvent import *

# Permets que le system d'evenement soit compatible avec GLFW
def on_resize(window, width, height):
    glViewport(0, 0, width, height)
    SystemEvenement.envoyer(WindowResizeEvent(width, height))
    i = Window.instance()
    if i is not None:
        i.__height = height
        i.__width = width

def scroll_callback(window, xoffset, yoffset):
    SystemEvenement.envoyer(MouseScrollEvent(xoffset, yoffset))

def mouse_button_callback(window, button, action, mods):
    SystemEvenement.envoyer(MousePressedEvent(button, action, mods,get_cursor_pos(window)))


def cursor_pos_callback(window, xpos, ypos):
    SystemEvenement.envoyer(MouseMovedEvent(xpos, ypos))

def key_press_callback(window, key, scancode, action, mods):
    SystemEvenement.envoyer(KeyPressedEvent(key, scancode, action, mods))

class Window:
    __instance = None

    def __init__(self, width: int, height: int, title: str):
        """
        cree une nouvelle fenetre OpenGL

        :param width: largeur de la fenêtre en pixels
        :param height: hauteur de la fenêtre en pixels
        :param title: titre de la fenêtre
        """
        if not init():
            raise Exception("GLFW n'a pas pu être initialisé")

        window_hint(CONTEXT_VERSION_MAJOR, 3)
        window_hint(CONTEXT_VERSION_MINOR, 3)
        window_hint(OPENGL_PROFILE, OPENGL_CORE_PROFILE)
        window_hint(VISIBLE, GL_FALSE)
        window_hint(OPENGL_FORWARD_COMPAT, GL_TRUE)
        # Anti-Aliasing
        window_hint(SAMPLES, 4)

        self.__window = create_window(width, height, title, None, None)
        self.__height = height
        self.__width = width

        if not self.__window:
            terminate()
            raise Exception("La fenêtre GLFW n'a pas pu être créée")

        make_context_current(self.__window)

        swap_interval(0)  # VSync

        # Mettre en place les events
        set_window_size_callback(self.__window, on_resize)
        set_scroll_callback(self.__window, scroll_callback)
        set_mouse_button_callback(self.__window, mouse_button_callback)
        set_cursor_pos_callback(self.__window, cursor_pos_callback)
        set_key_callback(self.__window, key_press_callback)

        # Configurer la vue initiale
        on_resize(self.__window, width, height)
        
        glEnable(GL_MULTISAMPLE)

        if Window.__instance is not None:
            raise PermissionError("Window ne peux pas avoir plus d'une instance")
        Window.__instance = self

    def show(self):
        show_window(self.__window)

    def supprimer(self):
        """
        Libère les ressources GLFW et ferme la fenêtre.
        """
        terminate()

    def devrait_fermer(self):
        """
        Vérifie si l'utilisateur a demandé la fermeture de la fenêtre.
        :return: True si la fenêtre doit être fermée, False sinon
        """
        return window_should_close(self.__window)

    def get_window(self):
        return self.__window

    def get_time(self) -> float:
        return get_time()

    def get_height(self) -> float:
        return self.__height

    def get_width(self) -> float:
        return self.__width

    def get_aspect(self):
        return self.__width/self.__height

    @staticmethod
    def instance() -> "Window":
        return Window.__instance  # type: ignore