import time
from src.event.event import *

# On utilise un decorateur pour enregister une class comme etant un evenement
@SystemEvenement.enregistrer_event
class CarteTirer:
    def __init__(self,idCarte:int) -> None:
        self.idCarte = idCarte
    
    def getIdCarte(self):
        return self.idCarte

# On utilise un autre decorateur pour dire d'executer la fonction quand l'event specifier est lancer
@SystemEvenement.ecouter("CarteTirer")
def afficher_carte_tirer(event:CarteTirer):
    print(event.getIdCarte())

# On utilise cette fonction pour déclancher un evenement
event = CarteTirer(10)
SystemEvenement.envoyer(event) # ou EventSystem.envoyer(CarteTirer(10))
time.sleep(1) # Est juste là pour simuler du travail après