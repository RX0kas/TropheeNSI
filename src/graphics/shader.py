import os.path

from OpenGL.GL import *
from ctypes import c_uint

class Shader:
    def __init__(self, shaderName: str):
        # Creer un programme OpenGL vide
        self.__program = glCreateProgram()

        # Lire le code source des fichiers
        contentV = self.__readShaderFile(shaderName + ".vert")
        contentF = self.__readShaderFile(shaderName + ".frag")

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

    def __readShaderFile(self, name: str):
        chemin = os.path.join(os.path.dirname(__file__),"shaders",f"{name}.glsl")
        try:
            return open(chemin).read()
        except FileNotFoundError:
            print(f"Fichier {chemin} n'existe pas")
            exit(1)
        except Exception as e:
            print(f"Erreur dans la lecture du fichier {chemin} : {e}")
            exit(1)

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

    def setVec3f(self, name: str, v0: float, v1: float, v2: float):
        glUniform3f(glGetUniformLocation(self.__program, name), v0, v1, v2)

    def setMat3f(self,name:str,matrix,transpose:bool=False):
        glUniformMatrix3fv(glGetUniformLocation(self.__program, name),1,GL_TRUE if transpose else GL_FALSE,matrix)