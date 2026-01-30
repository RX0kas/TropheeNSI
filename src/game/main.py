from deck import Deck
from carte import Carte
from jeu import Jeu

class Main:

    def __init__(self):
        self.jeus : list[Jeu] = []

    def __str__(self):
        affichage = ""
        for jeu in self.jeus:
            affichage = affichage + str(jeu) + " / "
        return affichage[:-4]


    def remplir_avec(self,deck:Deck):
        for _ in range(5-len(self.jeus)):
            self.tirer_jeu(deck)

    def tirer_jeu_depuis(self,deck: Deck):
        if deck.nb_carte >1:
            self.jeus.append(Jeu(deck.tirer_carte(),deck.tirer_carte()))

    def defausser(self, cible, deck):
        cible = cible.sort(reverse=True)
        for ind in cible:
            self.jeus.pop(ind)
        self.remplir_avec(deck)

    def jouer(self,cible,deck):
        jeu_jouer = []
        for ind in cible:
            self.jeus[ind].jouer(deck)
            if self.jeus[ind].val !=0:
                jeu_jouer.append(self.jeus[ind])
