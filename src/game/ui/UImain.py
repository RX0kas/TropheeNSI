from src.game.deck import Deck
from src.game.ui.UIjeu import UIJeu
from src.game.main import Main

class UIMain(Main):
    def __init__(self):
        super().__init__()
        self.jeux: list[UIJeu] = []
        self.choix = ""
        self.jeu_en_cours = -1
        self.playing = False
        self.cible = None
        self.current_jeu_index = 0
        self.played_games = []

    def tirer_jeu_depuis(self, deck: Deck):
        if deck.nb_carte() > 1:
            self.jeux.append(UIJeu(deck.tirer_carte(), deck.tirer_carte()))
        elif len(self.jeux) == 0:
            return "perdu"

    def jouer(self, cible, deck):
        """
        :return: -1 si il ne faut pas compter les points, le nombre de point sinon
        """
        if self.cible is None:
            self.cible = cible
            self.current_jeu_index = 0
            self.played_games = []
            self.playing = True
            self.jeu_en_cours = -1

        if not self.playing:
            return 0

        if self.current_jeu_index >= len(self.cible):
            total_points = 0
            if self.played_games:
                type_manche = self.detect_type_manche(self.played_games)
                score_base = self.dict_point[type_manche][0]
                multiplicateur = self.dict_point[type_manche][1]
                total_points = (score_base + sum(j.val for j in self.played_games)) * multiplicateur
            else:
                print("Aucun jeu ne rapporte de point")

            self.cible = None
            self.playing = False
            self.jeu_en_cours = -1
            self.choix = ""
            return total_points

        game_idx = self.cible[self.current_jeu_index]
        if game_idx >= len(self.jeux):
            self.current_jeu_index += 1
            return -1

        current_game = self.jeux[game_idx]

        self.jeu_en_cours = game_idx

        if self.choix not in ["p", "s"]:
            return -1

        # prendre
        if self.choix == "p":
            if not current_game.jouer_ui(deck, "p"):
                return -1
            if current_game.val == 0:
                self.current_jeu_index += 1
            self.choix = ""
            return -1

        # rester
        elif self.choix == "s":
            if current_game.val != 0:
                self.played_games.append(current_game)
            self.current_jeu_index += 1
            self.choix = ""
            return -1

        return -1