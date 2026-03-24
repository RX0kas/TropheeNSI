from math import radians
from src.graphics.texture import TextureManager
from src.graphics.sprite import Sprite
from src.graphics.sprite_renderer import SpriteRenderer
from src.graphics.ui.bouton import Bouton
from src.graphics.text.Text import Texte
from src.game.gameManager import GameManager
from src.game.carte import Carte
from os.path import join
from src.math.vectors import *

class UIManager:
    """
    Class qui sert a dessiner l'interface
    """
    __spriteCarte:dict[str,Sprite] = {}
    __boutonSelection:list[Bouton] = [] #type: ignore
    __spriteRendererRef:SpriteRenderer = None #type: ignore
    __gameManagerRef:GameManager = None #type: ignore
    
    @classmethod
    def get_card_sprite(cls,val:str|int,cou:str|int) -> Sprite:
        carte = None
        if isinstance(val,str) and isinstance(cou,str):
            carte = cls.__spriteCarte.get(val+cou)
        elif isinstance(val,int) and isinstance(cou,int):
            valStr:str = Carte.dict_transi_val[val]
            couStr:str = Carte.dict_transi_cou[cou]
            carte = cls.__spriteCarte.get(valStr+couStr)
        assert carte!=None,f"Erreur dans la creation de l'id de la carte: val:{val},cou:{cou}"
        
        return carte
    
    @classmethod
    def english_to_french(cls,couleurEnglais) -> str:
        if couleurEnglais=="hearts": return "coeur"
        if couleurEnglais=="diamonds": return "carreau"
        if couleurEnglais=="spades": return "pique"
        if couleurEnglais=="clubs": return "trèfle"
        if couleurEnglais=="V": return "J"
        if couleurEnglais=="D": return "Q"
        if couleurEnglais=="R": return "K"
        if couleurEnglais=="A": return "A"
        if couleurEnglais=="10": return "10"
        return "notfound"

    @classmethod
    def load_cards(cls):
        for cou in ["clubs","diamonds","hearts","spades"]:
            for num in range(2,10):
                id = str(num)+cls.english_to_french(cou)
                sprite = Sprite(join("assets",f"card_{cou}_0{num}.png"))
                cls.__spriteCarte[id] = sprite
                        
            for num in ["10","V","D","R","A"]:
                id = str(num)+cls.english_to_french(cou)
                sprite = Sprite(join("assets",f"card_{cou}_{cls.english_to_french(num)}.png"))
                cls.__spriteCarte[id] = sprite
        

        for i in range(5):
            cls.__boutonSelection.append(Bouton(join("assets","background_button.png"),enable=False))

    

    @classmethod
    def setupSprite(cls,sprite:Sprite,idxJeu:int,idxCarte:int):
        sprite.taille = 20
        if idxCarte:
            sprite.rotation = radians(-15)
            sprite.position = Vec2(-60+30*idxJeu,-20)
        elif idxCarte==0:
            sprite.rotation = radians(15)
            sprite.position = Vec2(-67+30*idxJeu,-20)
        
    
    @classmethod
    def draw_cards(cls):
        if cls.__spriteRendererRef is None:
            from src.core.application import Application
            cls.__spriteRendererRef = Application.get_instance().get_sprite_renderer()
        if cls.__gameManagerRef is None:
            from src.core.application import Application
            cls.__gameManagerRef = Application.get_instance().get_game_manager()

        cls.__draw_main_proposer()
    
    
    @classmethod
    def __draw_main_proposer(cls):
        jeuxProposes = [j for j in cls.__gameManagerRef.manche.main.jeux]
        for i in range(len(jeuxProposes)):
            # on obtient les sprites des deux cartes
            jeu = jeuxProposes[i]
            cartes = jeu.cartes
            sprite1 = cls.get_card_sprite(cartes[0].val,cartes[0].cou)
            sprite2 = cls.get_card_sprite(cartes[1].val,cartes[1].cou)
            cls.setupSprite(sprite1,i,0)
            cls.setupSprite(sprite2,i,1)
            cls.__spriteRendererRef.envoyer(sprite1)
            cls.__spriteRendererRef.envoyer(sprite2)
            cls.__draw_bouton_selection(i)

    @classmethod
    def __draw_bouton_selection(cls,idxJeu:int):
        pos = Vec2(-62+30*idxJeu,-40)
        bouton = cls.__boutonSelection[idxJeu]
        bouton.taille = Vec2(20,10)
        bouton.position = pos
        cls.__spriteRendererRef.envoyer(bouton)
        Texte.render_text("selectionner",pos.x,pos.y,Vec2(20,10),Vec3(1,1,1))