from src.game.carte import Carte
from src.game.deck import Deck
from src.game.jeu import Jeu


class UIJeu(Jeu):

    def __init__(self, c1: Carte, c2: Carte):
        super().__init__(c1, c2)

    def jouer_ui(self, deck: Deck,choix:str) -> bool:
        """
        :return True si le joueur a jouer
        """
        from src.core.application import Application
        nb_as = sum(1 for c in self.cartes if c.val == 1)

        if deck.est_vide():
            Application.get_instance().get_game_manager().perdu()
            return False

        if choix == "s":
            return True

        nvll_carte = deck.tirer_carte()
        if nvll_carte is None:
            Application.get_instance().get_game_manager().perdu()
            return False

        self.cartes.append(nvll_carte)
        self.val += self.dict_transi_val_point[nvll_carte.val]
        if nvll_carte.val == 1:
            nb_as += 1

        if self.val > 21:
            if nb_as == 0:
                self.val = 0
                self.cartes = []
            else:
                nb_as -= 1
                self.val -= 10
        return True