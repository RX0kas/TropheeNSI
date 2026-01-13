from OpenGL.GL import *
from ctypes import c_uint

from src.math.matrices import *
from src.math.vectors import *


class Shader:
    def __init__(self, contentV: str,contentF:str):
        # Creer un programme OpenGL vide
        self.__program = glCreateProgram()

        if contentV is None:
            print("Erreur dans la lecture du fichier vertex shader")
            exit(1)
        if contentF is None:
            print("Erreur dans la lecture du fichier fragment shader")
            exit(1)

        # On compile le code des shaders
        vertexShader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertexShader, contentV)
        glCompileShader(vertexShader)
        if glGetShaderiv(vertexShader, GL_COMPILE_STATUS) != GL_TRUE:
            print(f"Erreur dans la compilation du vertex shader: {glGetShaderInfoLog(vertexShader)}")
            exit(1)

        fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragmentShader, contentF)
        glCompileShader(fragmentShader)
        if glGetShaderiv(fragmentShader, GL_COMPILE_STATUS) != GL_TRUE:
            print(f"Erreur dans la compilation du fragment shader: {glGetShaderInfoLog(fragmentShader)}")
            exit(1)

        # On créé la pipeline graphique
        glAttachShader(self.__program, vertexShader)
        glAttachShader(self.__program, fragmentShader)
        glLinkProgram(self.__program)

        # verifier que tout est bien lier
        if glGetProgramiv(self.__program, GL_LINK_STATUS) != GL_TRUE:
            print(f"Erreur dans la liaison du programme: {glGetProgramInfoLog(self.__program)}")
            exit(1)

        # on supprime les shaders car ils ne sont plus nécessaires une fois lies au programme
        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)

    def use(self):
        glUseProgram(self.__program)

    def getProgram(self) -> int:
        """
        Retourne l'identifiant OpenGL du programme de shaders.
        """
        return self.__program # type: ignore

    def setBool(self, name: str, value: bool):
        glUniform1i(glGetUniformLocation(self.__program, name), value)

    def setInt(self, name: str, value: int):
        glUniform1i(glGetUniformLocation(self.__program, name), value)

    def setUInt(self, name: str, value: c_uint):
        """
        definit un uniforme entier non signé (rarement utiliser).
        Non signé veut dire qu'il n'y a pas de nombre negatif (jsp si tu le savais donc au cas ou)
        """
        glUniform1ui(glGetUniformLocation(self.__program, name), value)

    def setFloat(self, name: str, value: float):
        glUniform1f(glGetUniformLocation(self.__program, name), value)

    def setVec2f(self, name: str, v0: float, v1: float):
        glUniform2f(glGetUniformLocation(self.__program, name), v0, v1)

    def setVec3f(self, name: str, v:Vec3):
        glUniform3f(glGetUniformLocation(self.__program, name), v.x, v.y, v.z)

    def setMat3f(self,name:str,matrix:Mat3):
        glUniformMatrix3fv(glGetUniformLocation(self.__program, name),1,GL_TRUE,matrix.getData())

    def setMat4f(self,name:str,matrix:Mat4):
        glUniformMatrix4fv(glGetUniformLocation(self.__program, name),1,GL_TRUE,matrix.getData())