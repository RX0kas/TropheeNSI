from deck import Deck
from carte import Carte
from jeu import Jeu
from main import Main



import random

class Manche:

    def __init__(self,point_cible : int ,deck : Deck,main : int = 4,deffausse : int = 3):
        self.__cible = point_cible
        self.__point = 0
        self.__nb_deck = deck
        self.__deck_deffause = Deck()
        self.__nb_main = main
        self.__deffausse = deffausse
        self.main = Main()

    def __get_cible(self) -> int:
        return self.__cible
    
    def __set_cible(self,cible : int) -> None :
        self.__cible = cible

    def __get_point(self) -> int:
        return self.__point
    
    def __set_point(self,point : int) -> None :
        self.__point = point

    def __get_deck(self) -> Deck:
        return self.__deck
    
    def __set_deck(self,deck : Deck) -> None :
        self.__deck = deck

    def __get_deck_deffause(self) -> Deck:
        return self.__deck_deffause
    
    def __set_deck_deffause(self,deck : Deck) -> None :
        self.__deck_deffause = deck
    
    def __get_nb_main(self) -> int:
        return self.__nb_main
    
    def __set_nb_main(self,main : int) -> None :
        self.__nb_main = main

    def __get_nb_deffausse(self) -> int:
        return self.__nb_deffausse
    
    def __set_nb_deffausse(self,deffausse : int) -> None :
        self.__nb_deffausse = deffausse

    cible = property(__get_cible,__set_cible)
    point = property(__get_point,__set_point)
    deck = property(__get_deck,__set_deck)
    deck = property(__get_deck_deffause,__set_deck_deffause)
    nb_main = property(__get_nb_main,__set_nb_main)
    nb_deffausse = property(__get_nb_deffausse,__set_nb_deffausse)

    def __str__(self):
        return f"Vous avez actuellement {self.point} points et devait faire {self.cible} point, pour cela il vous reste {self.nb_main} mains et {self.nb_deffausse} déffausses"
    
    def jouer_manche(self):
        print(f"Dans cette manche vous avez {self.nb_main} mains et {self.nb_deffausse} déffausses pour faire {self.cible} points")
        self.deck.melanger()
        self.main.remplir_avec(self.deck)
        print(self.main)
        decision_j_d = self.decision_j_d()
        while self.nb_deffausse==0 or decision_j_d != "j":
            decision_j_d = self.decision_j_d()
        cible = self.decision_cible()
        if decision_j_d == "d":
            self.deffausser(cible)
        pass

    def dead(self) -> None:
        del self

    @staticmethod
    def decision_j_d():
        dec = ""
        while dec not in ["j","d"]:
            dec = input("j ou d")
        return dec
    
    @staticmethod
    def decision_cible(nb_jeu):
        dec = []
        while len(dec)<1:
            nvll_cible = input("nvll_cible")
            if nvll_cible in [str(x) for x in range(1,nb_jeu+1)]:
                dec.append(int(nvll_cible))
        while len(dec)<3:
            nvll_cible = input("nvll_cible ou s :stop")
            if nvll_cible in [str(x) for x in range(nb_jeu)] and nvll_cible not in dec:
                dec.append(int(nvll_cible)-1)
            if nvll_cible == "s":
                break
        return dec
    
    def deffausser(self,cible):
        self.nb_deffausse -= 1
        self.main.deffausser(cible,self.deck)
    

        

    
