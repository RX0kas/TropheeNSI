from carte import Carte
from deck import Deck

class Jeu:

    dict_transi_val_point= {1:11,2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:10,12:10,13:10}

    def __init__(self,c1 : Carte,c2 : Carte):
        self.cartes = [c1,c2]
        self.val = self.c_val()

    def __str__(self):
        affichage = ""
        for carte in self.cartes:
            affichage = affichage + str(carte) + " , "
        return affichage[:-4]
    
    def c_val(self) -> int:
        val = 0
        for carte in self.cartes:
            val += self.dict_transi_val_point[carte.val]
        return val
    
    def jouer(self,deck:Deck):
        nb_as = 0
        for carte in self.cartes:
            if carte.val == 1:
                nb_as += 1
        for _ in range(21):
            print(self,self.val,sep= ",Total:")
            dec = ""
            while dec not in ["p","s"]:
                dec = input("piocher :p ou stop :s")
            if dec == "s":
                print("jeu validé")
                break
            if dec == "p":
                if deck.est_vide():
                    print("plus de carte dans le deck")
                else :
                    nvll_carte = deck.tirer_carte()
                    self.val += self.dict_transi_val_point[nvll_carte.val]
                    if nvll_carte.val == 1:
                        nb_as += 1
                    self.cartes.append(nvll_carte)
            if self.val >21:
                if nb_as == 0:
                    print(self,self.val,sep= ",Total:")
                    self.val = 0
                    print("jeu mort")
                    self.cartes = []
                    break
                nb_as -= 1
                val -= 1
            
        
    
