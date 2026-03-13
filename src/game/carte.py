class Carte:

    dict_transi_val = {
        1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",
        8:"8",9:"9",10:"10",11:"V",12:"D",13:"R"
    }

    dict_transi_cou = {
        1:"coeur",
        2:"carreau",
        3:"pique",
        4:"trèfle"
    }

    def __init__(self, val: int, couleur: int):
        self.__val = val
        self.__cou = couleur

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, v):
        self.__val = v

    @property
    def cou(self):
        return self.__cou

    @cou.setter
    def cou(self, c):
        self.__cou = c

    def __str__(self):
        return f"{self.dict_transi_val[self.val]} de {self.dict_transi_cou[self.cou]}"