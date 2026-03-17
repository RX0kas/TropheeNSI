from src.graphics.texture import TextureManager
from src.graphics.sprite import Sprite
from src.graphics.sprite_renderer import SpriteRenderer
from src.game.carte import Carte
from os.path import join

class UIManager:
    """
    Class qui sert a dessiner l'interface
    """
    __spriteCarte:dict[str,Sprite] = {}
    __spriteRendererRef = None
    
    @classmethod
    def get_card_sprite(cls,val:str|int,cou:str|int) -> Sprite:
        carte = None
        if isinstance(val,str) and isinstance(cou,str):
            carte = cls.__spriteCarte.get(val+cou)
        elif isinstance(val,int) and isinstance(cou,int):
            valStr:str = Carte.dict_transi_val[val]
            couStr:str = Carte.dict_transi_cou[cou]
            carte = cls.__spriteCarte.get(valStr+couStr)
        assert carte!=None,"Erreur dans la creation de l'id de la carte"
        
        return carte
    
    @classmethod
    def english_to_french(cls,couleurEnglais) -> str:
        if couleurEnglais=="hearts": return "coeur"
        if couleurEnglais=="diamonds": return "carreau"
        if couleurEnglais=="spades": return "pique"
        if couleurEnglais=="clubs": return "trèfle"
        return "notfound"

    @classmethod
    def load_cards(cls):
        for cou in ["clubs","diamonds","hearts","spades"]:
            for num in range(2,10):
                id = str(num)+cls.english_to_french(cou)
                sprite = Sprite(join("assets",f"card_{cou}_0{num}.png"))
                cls.__spriteCarte[id] = sprite
                        
            for num in ["10","A","J","K","Q"]:
                id = str(num)+cls.english_to_french(cou)
                sprite = Sprite(join("assets",f"card_{cou}_{num}.png"))
                cls.__spriteCarte[id] = sprite
    
    
    @classmethod
    def draw_cards(cls):
        if cls.__spriteRendererRef is None:
            from src.core.application import Application
            cls.__spriteRendererRef = Application.get_instance().get_sprite_renderer()
        
        cls.__draw_main_proposer()
    
    
    @classmethod
    def __draw_main_proposer(cls):
        pass