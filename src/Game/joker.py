from src.graphics.sprite import Sprite
from carte import Carte

class Joker:

    def __init__(self):
        self.name : str|None = None
        self.valeur : int|None = None
        self.text : str|None = None
        self.sprite : Sprite|None = None
        self.place : int = 0 #{0: innesistant, 1:non présent, 2: posséder, 3: shop}
    
    def afficher_joker(self):
        pass

    def afficher_texte_joker(self):
        pass


    #évènement vide à modifié en sous-class


    def debut_manche(self):
        pass

    def fin_manche(self):
        pass

    def carte_debut_activation(self,c : Carte):
        pass

    def carte_activer(self,c : Carte):
        pass

    def carte_fin_activation(self,c : Carte):
        pass

    def main_jouer(self, type_main: int):
        pass

    def main_gagnante_jouer(self, type_main: int):
        pass

