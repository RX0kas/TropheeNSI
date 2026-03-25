from src.game.deck import Deck
from src.game.ui.UIjeu import UIJeu
from src.game.main import Main


class UIMain(Main):
    def __init__(self):
        super().__init__()
        self.jeux: list[UIJeu] = []
        self.choix = ""

    def tirer_jeu_depuis(self, deck: Deck):
        if deck.nb_carte() > 1:
            self.jeux.append(UIJeu(deck.tirer_carte(), deck.tirer_carte()))
        elif len(self.jeux) == 0:
            return "perdu"


    def jouer(self, cible, deck):
        """
        :return: -1 si il ne faut pas compter les points, le nombre de point sinon
        """
        if self.choix not in ["p", "s"]:
            return -1

        jeu_jouer = []
        for ind in cible:
            if ind < len(self.jeux):
                self.jeux[ind].jouer_ui(deck,self.choix)
                if self.jeux[ind].val != 0:
                    jeu_jouer.append(self.jeux[ind])

        if len(jeu_jouer) == 0:
            print("Aucun jeu ne rapporte de point")
            return 0

        type_manche = self.detect_type_manche(jeu_jouer)

        score_base = self.dict_point[type_manche][0]
        multiplicateur = self.dict_point[type_manche][1]
        total_points = (score_base + sum(j.val for j in jeu_jouer)) * multiplicateur

        self.choix = ""
        return total_points