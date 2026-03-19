from src.game.carte import Carte
from src.game.deck import Deck

class Jeu:

    dict_transi_val_point = {1:11,2:2,3:3,4:4,5:5,6:6,7:7,
                             8:8,9:9,10:10,11:10,12:10,13:10}

    def __init__(self, c1: Carte, c2: Carte):
        self.cartes = [c1, c2]
        self.val = self.c_val()

    def __str__(self):
        return " , ".join(str(c) for c in self.cartes)

    def c_val(self):
        return sum(self.dict_transi_val_point[c.val] for c in self.cartes)

    def jouer(self, deck: Deck):
        nb_as = sum(1 for c in self.cartes if c.val == 1)

        while True:
            print(self, ",Total:", self.val)
            if deck.est_vide():
                print("Plus de cartes dans le deck")
                break

            dec = ""
            while dec not in ["p","s"]:
                dec = input("piocher :p ou stop :s ")

            if dec == "s":
                print("jeu validé")
                break

            nvll_carte = deck.tirer_carte()
            if nvll_carte is None:
                print("Plus de cartes dans le deck")
                break

            self.cartes.append(nvll_carte)
            self.val += self.dict_transi_val_point[nvll_carte.val]
            if nvll_carte.val == 1:
                nb_as += 1

            if self.val > 21:
                if nb_as == 0:
                    print(self, ",Total:", self.val)
                    print("jeu mort")
                    self.val = 0
                    self.cartes = []
                    break
                nb_as -= 1
                self.val -= 10

    def reel(self):
        val_cartes = sorted([c.val for c in self.cartes])
        val_cou_carte = sorted([(c.val, c.cou) for c in self.cartes], key=lambda x:x[0])
        return [self.val, len(self.cartes), val_cartes, val_cou_carte]

            
        
    
