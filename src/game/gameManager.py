from src.game.deck import Deck

class GameManager:
    def __init__(self):
        self.deck = Deck()
        self.deck.reset_52()
        self.cib = 100
        self.cycle = 0
        self.manche = Manche(point_cible=cib, deck=mon_deck, main=4, defausse=3)
    
    # appeler avant d'ouvrir l'application
    def setup(self):
        pass