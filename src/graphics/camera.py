from src.core.window import Window
from src.math.matrices import *
from src.math.vectors import *
from math import cos,sin

class Camera:
    position = Vec2() # Centre de la caméra
    zoom = 1.0
    rotation = 0.0 # rotation en degrés

    def __init__(self):
        pass

    def get_projection_matrix(self) -> Mat4:
        """
        :param hauteur:
        :return: une matrice qui va servir a definir ce que l'on peut voir sur l'écran
        """
        aspect = Window.instance().get_aspect()
        hauteurVue = 10 # hauteur de la fenetre lorsque le zoom est de 1

        hauteur = hauteurVue / self.zoom
        largeur = hauteur * aspect
        return Mat4.orthographic(-largeur/2,largeur/2,-hauteur/2,hauteur/2)

    def get_view_matrix(self) -> Mat4:
        """
        :return:
        """

        view = Mat4()
        cosrot = cos(self.rotation)
        sinrot = sin(self.rotation)

        view[0,0] = cosrot
        view[0,1] = -sinrot
        view[1,0] = sinrot
        view[1,1] = cosrot
        view[2,2] = 1.0
        view[3,3] = 1.0

        view[0,3] = -self.position.x * cosrot - self.position.y * sinrot
        view[1,3] = self.position.x * sinrot - self.position.y * cosrot

        return view

    def get_view_projection_matrix(self) -> Mat4:
        return self.get_projection_matrix() * self.get_view_matrix()
