from ctypes import sizeof,c_float
from math import cos,sin

from src.math.vectors import Vec2,Vec4


class Mat4:
    size = 4 # present car j'ai copier coller Mat4 pour faire les autres
    
    def __init__(self, data=None):
        taille = self.size**2
        if data is None:
            self._data = [0.0] * taille
        else:
            if len(data) != taille:
                raise ValueError(f"Mat{self.size} doit etre exactement de {taille} valeurs")
            self._data = list(data)

    @classmethod
    def get_gpu_memory_size(cls):
        return (cls.size**2)*sizeof(c_float)

    @classmethod
    def __pos_to_index(cls,x, y):
        return x*cls.size+y

    @classmethod
    def __index_to_pos(cls,i):
        return i%cls.size, i//cls.size

    def __iter__(self): # sert a pouvoir iterer sur la matrice
        return iter(self._data)

    def __getitem__(self, key) -> float: # pour faire Mat4[1,4]
        i, j = key
        return self._data[self.__pos_to_index(i, j)]

    def __setitem__(self, key, value:float): # pour faire Mat4[1,4] = 5
        i, j = key
        self._data[self.__pos_to_index(i, j)] = value

    def __repr__(self): # debug
        return f"Matrix{self.size}x{self.size}({self._data})"

    def __add__(self, other):
        result = [self[i,j] + other[i,j] for i in range(self.size) for j in range(self.size)] # en deux lignes car un generateur n'a pas de len() -> "TypeError: object of type 'generator' has no len()"
        return self.__class__(result) # Parcours la matrice et on ajoute les cases

    def __mul__(self, other):
        if isinstance(other,Vec4):
            result = Vec4()
            for i in range(self.size):
                for k in range(self.size):
                    result[i] += self[i,k]*other[k]
                    
            return result
            
        result = self.__class__() # on créé une matrice vide
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    result[i,j] += self[i,k] * other[k,j] # On multiplie les colones par les colones
        return result


    def __eq__(self, other):
        return self._data == other._data

    def getData(self):
        return self._data

    @classmethod
    def orthographic(cls,left:float,right:float,bottom:float,top:float):
        """
        Src https://github.com/g-truc/glm/blob/b1fed407864225653dae04674f04014c92287a26/glm/ext/matrix_clip_space.inl
        """
        mat = Mat4()

        mat[0, 0] = 2.0 / (right - left)
        mat[1, 1] = 2.0 / (top - bottom)
        mat[2, 2] = -1.0
        mat[3, 3] = 1.0

        mat[3, 0] = -(right + left) / (right - left)
        mat[3, 1] = -(top + bottom) / (top - bottom)

        return mat


class Mat3(Mat4):
    size = 3

    def __init__(self, data=None):
        super().__init__(data)

    @classmethod
    def model(cls, angle: float, pos: Vec2, taille: Vec2):
        """
        Matrice 3x3 finale:
        [ cosθ * sx   -sinθ * sy   position.x ]
        [ sinθ * sx    cosθ * sy   position.y ]
        [     0            0            1      ]

        sx, sy = taille
        θ = angle
        Src https://en.wikipedia.org/wiki/Transformation_matrix#Examples_in_2_dimensions
        """
        mat = Mat3()

        cosO = cos(angle)
        sinO = sin(angle)
        
        mat[0, 0] = cosO * taille.x
        mat[1, 0] = sinO * taille.x
        mat[2, 0] = 0.0

        mat[0, 1] = -sinO * taille.y
        mat[1, 1] = cosO * taille.y
        mat[2, 1] = 0.0

        mat[0, 2] = pos.x
        mat[1, 2] = pos.y
        mat[2, 2] = 1.0

        return mat