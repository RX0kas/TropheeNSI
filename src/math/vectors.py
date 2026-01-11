
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

    # TODO: ajouter d'autres methodes