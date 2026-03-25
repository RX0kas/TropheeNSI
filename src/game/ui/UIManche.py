from src.game.deck import Deck
from src.game.manche import Manche
from src.game.ui.UImain import UIMain


class UIManche(Manche):


    def __init__(self, point_cible: float, deck: Deck, main=4, defausse=3):
        super().__init__(point_cible, deck, main, defausse)
        self.main = UIMain()

    def jouer_tour(self):
        print("\nJeux disponibles :")
        print(self.main)

        print(f"Mains restantes : {self.nb_main} | Défausses restantes : {self.nb_defausse}")

        decision = self.decision_j_d()
        cible = self.decision_cible(len(self.main.jeux))

        if decision == "d":
            if self.nb_defausse <= 0:
                print("Vous n'avez plus de défausses disponibles, vous devez jouer.")
                decision = "j"

        if decision == "d":
            self.nb_defausse -= 1
            if self.main.defausser(cible, self.deck, self.deck_defausse) == "perdu":
                print("Plus de cartes pour défausser")
                return False
        else:
            self.nb_main -= 1
            points = self.main.jouer(cible, self.deck)
            self.point += points
            print(f"Score total: {self.point}")

            self.main.defausser(cible, self.deck, self.deck_defausse)

            if self.point >= self.cible:
                print("Victoire !")
                return True

        if self.main.remplir_avec(self.deck) == "perdu":
            print("Plus assez de cartes pour compléter la main, vous jouez avec ce qu'il reste.")

    @staticmethod
    def decision_j_d():
        dec = ""
        while dec not in ["j","d"]:
            dec = input("jouer (j) ou défausser (d) ? ")
        return dec

    @staticmethod
    def decision_cible(nb_jeu):
        dec = []
        while len(dec) == 0:
            nv = input("Choisir un jeu : ")
            if nv.isdigit() and 1 <= int(nv) <= nb_jeu:
                dec.append(int(nv)-1)
        while len(dec) < 3:
            nv = input("Autre jeu ou s pour stop : ")
            if nv == "s":
                return dec
            if nv.isdigit():
                ind = int(nv)-1
                if 0 <= ind < nb_jeu and ind not in dec:
                    dec.append(ind)
        return dec