from deck import Deck
from carte import Carte
from jeu import Jeu

class Main:

    dict_point ={"simple":[5,1],"double":[10,2],"triple":[20,3],"s double":[30,3],"s triple":[40,5],"u double":[50,5],"u triple":[75,7],"p double":[80,8],"p triple":[150,10]}

    def __init__(self):
        self.jeus : list[Jeu] = []

    def __str__(self):
        affichage = ""
        for jeu in self.jeus:
            affichage = affichage + str(jeu) + " / "
        return affichage[:-3]


    def remplir_avec(self,deck:Deck):
        for _ in range(5-len(self.jeus)):
            if self.tirer_jeu_depuis(deck) in ["perdu"]:
                return "perdu"
        

    def tirer_jeu_depuis(self,deck: Deck):
        if deck.nb_carte() >1:
            self.jeus.append(Jeu(deck.tirer_carte(),deck.tirer_carte()))
        elif len(self.jeus) == 0:
            return "perdu"

    def deffausser(self,cible,deck,deck_deffausse):
        cible = cible.sort(reverse=True)
        for ind in cible:
            for carte in self.jeus[ind]:
                deck_deffausse.rajouter_carte(carte)
            self.jeus.pop(ind)
        if self.tirer_jeu_depuis(deck) in ["perdu"]:
            return "perdu"

    def jouer(self,cible,deck):
        jeu_jouer = []
        for ind in cible:
            self.jeus[ind].jouer(deck)
            if self.jeus[ind].val !=0:
                jeu_jouer.append(self.jeus[ind])
            if len(jeu_jouer) == 0:
                print("Aucun jeu ne rapporte de point")
                return 0
            if len(jeu_jouer) == 1:
                point = (self.dict_point["simple"][0] + jeu_jouer[0].val) * self.dict_point["simple"][2]
            else:
                reel_jeu_jouer = [jeu.reel() for jeu in jeu_jouer]
                point = 0
                for jeu in reel_jeu_jouer:
                    point += jeu[0]
                if len(self.get_elms_a_ind(reel_jeu_jouer,3)) == 3 and len(set(self.get_elms_a_ind(reel_jeu_jouer,3))) == 1:
                    point = (point + self.dict_point["p triple"][0]) * self.dict_point["p triple"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,3)) != len(set(self.get_elms_a_ind(reel_jeu_jouer,3))):
                    point = (point + self.dict_point["p double"][0]) * self.dict_point["p double"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,2)) == 3 and len(set(self.get_elms_a_ind(reel_jeu_jouer,2))) == 1:
                    point = (point + self.dict_point["u triple"][0]) * self.dict_point["u triple"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,2)) != len(set(self.get_elms_a_ind(reel_jeu_jouer,2))):
                    point = (point + self.dict_point["u double"][0]) * self.dict_point["u double"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,1)) == 3 and len(set(self.get_elms_a_ind(reel_jeu_jouer,1))) == 1:
                    point = (point + self.dict_point["s triple"][0]) * self.dict_point["s triple"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,1)) != len(set(self.get_elms_a_ind(reel_jeu_jouer,1))):
                    point = (point + self.dict_point["s double"][0]) * self.dict_point["s double"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,0)) == 3 and len(set(self.get_elms_a_ind(reel_jeu_jouer,0))) == 1:
                    point = (point + self.dict_point["triple"][0]) * self.dict_point["triple"][1]
                elif len(self.get_elms_a_ind(reel_jeu_jouer,0)) != len(set(self.get_elms_a_ind(reel_jeu_jouer,0))):
                    point = (point + self.dict_point["double"][0]) * self.dict_point["double"][1]
            print(f"Vous avez fait {point} points")
            return point
        

    @staticmethod
    def get_elms_a_ind(liste,ind):
        return [x[ind] for x in liste]
                
                
        
        
        

