import math
from ctypes import sizeof,c_float


class Vec2:
    def __init__(self, x:float=0, y:float=0):
        self.x = x
        self.y = y

    def __getitem__(self, key) -> float: # pour faire Vec2[1]
        assert key in [0,1]
        return self.x if key==0 else self.y

    def __setitem__(self, key, value:float): # pour faire Vec2[1] = 5
        assert key in [0, 1]
        if key: # key=1
            self.y = value
        else:
            self.x = value

    @classmethod
    def get_gpu_memory_size(cls):
        return 2*sizeof(c_float)

    def distance(self,other:"Vec2") -> float:
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    
class Vec3:
    def __init__(self, x:float=0, y:float=0,z:float=0):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, key) -> float: # pour faire Vec3[1]
        assert key in [0,1,2]
        if key==0:
            return self.x
        elif key==1:
            return self.y
        else:
            return self.z
        
    def __setitem__(self, key, value:float) -> None: # pour faire Vec3[1] = 5
        assert key in [0,1,2]
        if key==0:
            self.x = value
        elif key==1:
            self.y = value
        else:
            self.z = value
    
    @classmethod
    def get_gpu_memory_size(cls):
        return 3*sizeof(c_float)
    
    def __noir(self):
        return Vec3()
    
    def __blanc(self):
        return Vec3(1,1,1)
    
    NOIR = property(__noir)
    BLANC = property(__blanc)
    
class Vec4:
    def __init__(self, x:float=0, y:float=0,z:float=0,w:float=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __getitem__(self, key) -> float: # pour faire Vec3[1]
        assert key in [0,1,2,3]
        if key==0:
            return self.x
        elif key==1:
            return self.y
        elif key==2:
            return self.z
        return self.w
        
    def __setitem__(self, key, value:float) -> None: # pour faire Vec4[1] = 5
        assert key in [0,1,2,3]
        if key==0:
            self.x = value
        elif key==1:
            self.y = value
        elif key==2:
            self.z = value
        else:
            self.w = value
    
    @classmethod
    def get_gpu_memory_size(cls):
        return 3*sizeof(c_float)