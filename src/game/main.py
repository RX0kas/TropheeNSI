from src.game.deck import Deck
from src.game.jeu import Jeu
from collections import Counter

class Main:

    dict_point = {
        "simple":[5,1],
        "double":[10,2],
        "triple":[20,3],
        "s double":[30,3],
        "s triple":[40,5],
        "u double":[50,5],
        "u triple":[75,7],
        "p double":[80,8],
        "p triple":[150,10]
    }

    def __init__(self):
        self.jeux: list[Jeu] = []

    def __str__(self):
        affichage = ""
        for i, j in enumerate(self.jeux):
            affichage += f"{i+1}: {j} (Total: {j.val})\n"
        return affichage.strip()

    def remplir_avec(self, deck: Deck):
        for _ in range(5 - len(self.jeux)):
            if self.tirer_jeu_depuis(deck) == "perdu":
                return "perdu"

    def tirer_jeu_depuis(self, deck: Deck):
        if deck.nb_carte() > 1:
            self.jeux.append(Jeu(deck.tirer_carte(), deck.tirer_carte()))
        elif len(self.jeux) == 0:
            return "perdu"

    def defausser(self, cible, deck, deck_defausse):
        cible.sort(reverse=True)
        for ind in cible:
            if ind < len(self.jeux):
                for c in self.jeux[ind].cartes:
                    deck_defausse.rajouter_carte(c)
                self.jeux.pop(ind)
        if self.tirer_jeu_depuis(deck) == "perdu":
            return "perdu"

    @staticmethod
    def detect_type_manche(jeu_jouer):
        liste_reel = [j.reel() for j in jeu_jouer]

        cartes_complet = [tuple(sorted(j[3])) for j in liste_reel]
        cartes_val = [tuple(sorted([c[0] for c in j[3]])) for j in liste_reel]
        score_nb = [(j[0], j[1]) for j in liste_reel]
        valeurs = [j[0] for j in liste_reel]

        n = len(jeu_jouer)

        counter_complet = Counter(cartes_complet)
        counter_val = Counter(cartes_val)
        counter_score = Counter(score_nb)
        counter_valeur = Counter(valeurs)

        if n == 3 and 3 in counter_complet.values():
            return "p triple"
        elif 2 in counter_complet.values():
            return "p double"
        elif n == 3 and 3 in counter_val.values():
            return "u triple"
        elif 2 in counter_val.values():
            return "u double"
        elif n == 3 and 3 in counter_score.values():
            return "s triple"
        elif 2 in counter_score.values():
            return "s double"
        elif n == 3 and 3 in counter_valeur.values():
            return "triple"
        elif 2 in counter_valeur.values():
            return "double"
        else:
            return "simple"

    def jouer(self, cible, deck):
        jeu_jouer = []
        for ind in cible:
            if ind < len(self.jeux):
                self.jeux[ind].jouer(deck)
                if self.jeux[ind].val != 0:
                    jeu_jouer.append(self.jeux[ind])

        if len(jeu_jouer) == 0:
            print("Aucun jeu ne rapporte de point")
            return 0

        type_manche = self.detect_type_manche(jeu_jouer)

        score_base = self.dict_point[type_manche][0]
        multiplicateur = self.dict_point[type_manche][1]
        total_points = (score_base + sum(j.val for j in jeu_jouer)) * multiplicateur

        print(f"Type de main : {type_manche}")
        print(f"Points obtenus cette main : {total_points}")
        return total_points
                
                
        
        
        

