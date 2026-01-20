from carte import Carte
import random

class Deck:

    def __init__(self) -> "Deck":
        self.__contenue : list[Carte] = []

    def __get_contenue(self) -> list[Carte]:
        return self.__contenue
    
    def __set_contenue(self,contenue : list[Carte]) -> None :
        self.__contenue = contenue

    contenue = property(__get_contenue,__set_contenue)
    
    def est_vide(self) -> bool:
        return self.nb_carte == 0
    
    def nb_carte(self) -> int:
        return len(self.contenue)
    
    def tirer_carte(self) -> Carte|None:
        if self.est_vide():
            return None
        return self.contenue.pop(0)
    
    def rajouter_carte(self,carte : Carte) -> None:
        self.contenue.append(carte)

    def melanger(self) -> None:
        cartes = self.contenue
        self.contenue = []
        while len(cartes) != 0:
            self.contenue.append(cartes.pop(random.randint(0,len(cartes)-1)))

    def reset_52(self) -> None:
        self.contenue = []
        for cou in range(1,5):
            for val in range(1,14):
                self.rajouter_carte(Carte(val,cou))
        self.melanger()

    def vider_dans(self,deck2 : "Deck"):
        while not self.est_vide():
            deck2.rajouter_carte(self.tirer_carte())

    def dead(self) -> None:
        del self

    
    



if __name__ == "__main__":
    mon_deck = Deck()
    # print(mon_deck.est_vide())
    # mon_deck.rajouter_carte(Carte(10,3))
    # mon_deck.rajouter_carte(Carte(13,2))
    # print(mon_deck.est_vide())
    # print(mon_deck.tirer_carte())
    # print(mon_deck.tirer_carte())
    # print(mon_deck.est_vide())
    # mon_deck.rajouter_carte(Carte(1,3))
    # mon_deck.rajouter_carte(Carte(3,2))
    # mon_deck.rajouter_carte(Carte(10,4))
    # mon_deck.rajouter_carte(Carte(13,1))
    # mon_deck.melanger()
    # print(mon_deck.tirer_carte())
    # print(mon_deck.tirer_carte())
    # print(mon_deck.tirer_carte())
    # print(mon_deck.tirer_carte())
    mon_deck.reset_52()
    for _ in range(10):
        print(mon_deck.tirer_carte())
