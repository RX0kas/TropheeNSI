import random
from src.game.carte import Carte

class Deck:

    def __init__(self):
        self.contenu: list[Carte] = []

    def est_vide(self):
        return self.nb_carte() == 0

    def nb_carte(self):
        return len(self.contenu)

    def tirer_carte(self):
        if self.est_vide():
            return None
        return self.contenu.pop(0)

    def rajouter_carte(self, carte: Carte):
        self.contenu.append(carte)

    def melanger(self):
        random.shuffle(self.contenu)

    def reset_52(self):
        self.contenu = []
        for cou in range(1,5):
            for val in range(1,14):
                self.rajouter_carte(Carte(val,cou))
        self.melanger()

    def vider_dans(self, deck2):
        while not self.est_vide():
            deck2.rajouter_carte(self.tirer_carte())