from src.game.deck import Deck
from src.game.ui.UIManche import UIManche

NONE = 0
JOUER_BTN = 1
DEFAUSSE_BTN = 2

class GameManager:
    def __init__(self):
        self.deck:Deck = Deck()
        self.deck.reset_52()
        self.cib = 100
        self.cycle = 0
        self.manche:UIManche = UIManche(point_cible=self.cib, deck=self.deck, main=4, defausse=3)

        self.running = False
        self.btn_pressed = NONE
        self.jeu_cibles = []
        self.en_attente_choix = False
        self.a_perdu = False
    
    # appeler avant d'ouvrir l'application
    def setup(self):
        self.manche.deck.melanger()
        self.manche.main.remplir_avec(self.deck)
        self.running = True
        self.en_attente_choix = False

    # appeler a chaque frame
    def update(self):
        if not self.running:
            return

        if self.manche.nb_main <= 0:
            self.perdu()

        self.manche.main.remplir_avec(self.deck)

        if self.en_attente_choix:
            self.__jouer()
            self.btn_pressed = NONE
        elif len(self.jeu_cibles):
            if self.btn_pressed == JOUER_BTN:
                self.__jouer()
            elif self.btn_pressed == DEFAUSSE_BTN:
                self.__defausser()
            self.btn_pressed = NONE

    def __jouer(self):
        points = self.manche.main.jouer(self.jeu_cibles, self.deck)
        # Si on a pas choisi
        if points == -1:
            self.en_attente_choix = True
            return

        self.en_attente_choix = False
        self.manche.nb_main -= 1
        self.manche.point += points

        self.manche.main.defausser(self.jeu_cibles, self.deck, self.manche.deck_defausse)

        if self.manche.point >= self.manche.cible:
            self.gagner()

        self.jeu_cibles = []


    def __defausser(self):
        if self.manche.nb_defausse > 0:
            self.manche.nb_defausse -= 1
            if self.manche.main.defausser(self.jeu_cibles, self.deck, self.manche.deck_defausse) == "perdu":
                print("Plus de cartes à defausser")
                self.perdu()

            self.jeu_cibles = []

    def perdu(self):
        self.running = False
        self.a_perdu = True

    def gagner(self):
        self.running = False
        # TODO: afficher et relancer en plus dure
        print("Gagner")