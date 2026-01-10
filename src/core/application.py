import glfw
from src.core.window import Window


class Application:
    VERSION = "0.0.1"

    def __init__(self):
        self.__fenetre = Window(800, 600, "Trophe NSI - " + Application.VERSION)

        from OpenGL.GL import glGetString, GL_VERSION
        try:
            print("PyOpenGL GL_VERSION:", glGetString(GL_VERSION))
        except Exception as e:
            print("PyOpenGL can't query GL_VERSION yet:", e)

    def run(self):
        from OpenGL.GL import glClearColor, glClear, GL_COLOR_BUFFER_BIT
        self.__fenetre.show()

        lastFrame = 0.0
        while not self.__fenetre.devrait_fermer():
            glfw.poll_events()
            currentFrame = self.__fenetre.getTime()
            deltaTime = currentFrame - lastFrame
            lastFrame = currentFrame

            glClearColor(0.2, 0.2, 0.2, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)
            glfw.swap_buffers(self.__fenetre.getWindow())

        self.__fenetre.supprimer()

    def stop(self):
        glfw.set_window_should_close(self.__fenetre.getWindow(), True)