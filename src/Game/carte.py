class Carte:

    dict_transi_val = {1:"A",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10",11:"V",12:"D",13:"R"}

    dict_transi_cou = {1:"coeur",2:"carreau",3:"pique",4:"trèfle"}

    def __init__(self,val : int, couleur : int) -> "Carte":
        self.__val : int = val
        self.__cou : int = couleur

    def __get_val(self) -> int:
        return self.__val
    
    def __set_val(self,val : int) -> None :
        self.__val = val

    def __get_cou(self) -> int:
        return self.__cou
    
    def __set_cou(self,couleur : int) -> None :
        self.__cou = couleur

    val = property(__get_val,__set_val)
    cou = property(__get_cou,__set_cou)

    def __str__(self) -> str:
        return f"{self.dict_transi_val[self.val]} de {self.dict_transi_cou[self.cou]}"
