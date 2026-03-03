from carte import Carte
import random

class Deck:

    def __init__(self) -> "Deck":
        self.__contenu : list[Carte] = []

    def __get_contenu(self) -> list[Carte]:
        return self.__contenu
    
    def __set_contenu(self,contenu : list[Carte]) -> None :
        self.__contenu = contenu

    contenu = property(__get_contenu,__set_contenu)
    
    def est_vide(self) -> bool:
        return self.nb_carte == 0
    
    def nb_carte(self) -> int:
        return len(self.contenu)
    
    def tirer_carte(self) -> Carte|None:
        if self.est_vide():
            return None
        return self.contenu.pop(0)
    
    def rajouter_carte(self,carte : Carte) -> None:
        self.contenu.append(carte)

    def melanger(self) -> None:
        cartes = self.contenu
        self.contenu = []
        while len(cartes) != 0:
            self.contenu.append(cartes.pop(random.randint(0,len(cartes)-1)))

    def reset_52(self) -> None:
        self.contenu = []
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
