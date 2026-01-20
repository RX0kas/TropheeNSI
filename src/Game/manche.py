from deck import Deck
from carte import Carte
import random

class Manche:

    def __init__(self,point_cible : int ,deck : Deck,main : int = 4,deffausse : int = 3):
        self.__cible = point_cible
        self.__point = 0
        self.__deck = deck
        self.__deck_deffause = Deck()
        self.__main = main
        self.__deffausse = deffausse

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
    
    def __get_main(self) -> int:
        return self.__main
    
    def __set_main(self,main : int) -> None :
        self.__main = main

    def __get_deffausse(self) -> int:
        return self.__deffausse
    
    def __set_deffausse(self,deffausse : int) -> None :
        self.__deffausse = deffausse

    cible = property(__get_cible,__set_cible)
    point = property(__get_point,__set_point)
    deck = property(__get_deck,__set_deck)
    deck = property(__get_deck_deffause,__set_deck_deffause)
    main = property(__get_main,__set_main)
    deffausse = property(__get_deffausse,__set_deffausse)

    def __str__(self):
        return f"Vous avez actuellement {self.point} points et devait faire {self.cible} point, pour cela il vous reste {self.main} mains et {self.deffausse} déffausses"
    
    def jouer_manche(self):
        print(f"Dans cette manche vous avez {self.main} mains et {self.deffausse} déffausses pour faire {self.cible} points")
        main : list[list[Carte]] = []
        self.deck.melanger()
        self.remplir_main(main)
        pass

    def dead(self) -> None:
        del self

    def tirer_jeu(self) -> list[Carte]|None:
        if self.deck.nb_carte >1:
            return [self.deck.tirer_carte(),self.deck.tirer_carte()]
        return None
    
    def remplir_main(self,main) -> None:
        for _ in range(5-len(main)):
            jeu = self.tirer_jeu()
            if jeu != None:
                main.append(self.tirer_jeu())
            elif len(main) == 0:
                print("Vous n'avez plus de carte, c'est perdu")
                self.dead()
            else :
                break

    def decission(self,mains : list[list[Carte]]) -> None:
        dec = ""
        while dec not in ["j","d"] or (dec == "d" and self.deffausse == 0):
            if self.deffausse != 0:
                dec = input("j:jouer ou d:deffause")
            else:
                dec = input("j:jouer")
        j1 = None
        j2 = None
        j3 = None
        while j1 not in [str(i) for i in range(1,len(mains)+1)]:
            j1 = input("Pour quel jeu?")
        if len(mains)>1:
            while (j2 not in [str(i) for i in range(1,len(mains)+1)] and j2 != "a") or j2 == j1:
                j2 = input("Pour quel jeu, différent que le premier, a:aucun?")
            if len(mains)>2 and j2 != "a":
                while (j3 not in [str(i) for i in range(1,len(mains)+1)] and j3 != "a") or j3 == j1 or j3 == j2:
                    j3 = input("Pour quel jeu, différent que des précedents, a:aucun?")
        jeu_joue = [x for x in [j1,j2,j3] if x not in [None,"a"]]
        if dec == "d":
            self.deffausser(mains,jeu_joue)
        if dec == "j":
            pass

    def deffausser(self,main : list[list[Carte]] ,cible : list[int]) -> None:
        cible.sort(reverse=True)
        for jeu in cible:
            main.pop(jeu-1)
        self.remplir_main(main)
        self.deffausse -=1
