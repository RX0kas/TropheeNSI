from math import radians

from src.graphics.sprite import Sprite
from src.graphics.sprite_renderer import SpriteRenderer
from src.graphics.text.Text import Texte
from src.graphics.ui.bouton import Bouton
from src.game.gameManager import GameManager
from src.game.carte import Carte
from os.path import join
from src.math.vectors import *

NONE = 0
JOUER_BTN = 1
DEFAUSSE_BTN = 2


class UIManager:
    """
    Class qui sert a dessiner l'interface
    """
    __spriteCarte: dict[str, Sprite] = {}
    __boutonSelection: list[Bouton] = []  # type: ignore
    __boutonJouer: Bouton = None  # type: ignore
    __boutonDefausse: Bouton = None  # type: ignore
    __boutonPrendre: Bouton = None  # type: ignore
    __boutonRester: Bouton = None  # type: ignore

    __spriteRendererRef: SpriteRenderer = None  # type: ignore
    __gameManagerRef: GameManager = None  # type: ignore

    __lastBtnPressed = NONE  # 1 -> Jouer, 2 -> défausser

    @classmethod
    def get_card_sprite(cls, val: str | int, cou: str | int) -> Sprite:
        carte = None
        if isinstance(val, str) and isinstance(cou, str):
            carte = cls.__spriteCarte.get(val + cou)
        elif isinstance(val, int) and isinstance(cou, int):
            valStr: str = Carte.dict_transi_val[val]
            couStr: str = Carte.dict_transi_cou[cou]
            carte = cls.__spriteCarte.get(valStr + couStr)

        return carte

    @classmethod
    def english_to_french(cls, couleurEnglais) -> str:
        if couleurEnglais == "hearts": return "coeur"
        if couleurEnglais == "diamonds": return "carreau"
        if couleurEnglais == "spades": return "pique"
        if couleurEnglais == "clubs": return "trèfle"
        if couleurEnglais == "V": return "J"
        if couleurEnglais == "D": return "Q"
        if couleurEnglais == "R": return "K"
        if couleurEnglais == "A": return "A"
        if couleurEnglais == "10": return "10"
        return "notfound"

    @classmethod
    def load_cards(cls):
        for cou in ["clubs", "diamonds", "hearts", "spades"]:
            for num in range(2, 10):
                id = str(num) + cls.english_to_french(cou)
                sprite = Sprite(join("assets", f"card_{cou}_0{num}.png"))
                cls.__spriteCarte[id] = sprite

            for num in ["10", "V", "D", "R", "A"]:
                id = str(num) + cls.english_to_french(cou)
                sprite = Sprite(join("assets", f"card_{cou}_{cls.english_to_french(num)}.png"))
                cls.__spriteCarte[id] = sprite

        for i in range(5):
            btn = Bouton(join("assets", "background_button.png"))

            def make_callback(idx):
                def callback(btn: Bouton):
                    if cls.__gameManagerRef.en_attente_choix:
                        return
                    jeu = cls.__gameManagerRef.manche.main.jeux[idx]
                    if jeu.val == 0:
                        return
                    if idx in cls.__gameManagerRef.jeu_cibles:
                        cls.__gameManagerRef.jeu_cibles.remove(idx)
                    else:
                        if len(cls.__gameManagerRef.jeu_cibles) == 3:
                            cls.__gameManagerRef.jeu_cibles.pop()
                        cls.__gameManagerRef.jeu_cibles.append(idx)

                return callback

            btn.ajouter_callback(make_callback(i))
            cls.__boutonSelection.append(btn)

        # Bouton Jouer
        cls.__boutonJouer = Bouton(join("assets", "jouer_btn.png"))
        cls.__boutonJouer.position = Vec2(-50, 22)
        cls.__boutonJouer.taille = Vec2(20, 10)

        def make_callback_j():
            def callback(btn: Bouton):
                cls.__gameManagerRef.btn_pressed = JOUER_BTN

            return callback

        cls.__boutonJouer.ajouter_callback(make_callback_j())

        # Bouton defausse
        cls.__boutonDefausse = Bouton(join("assets", "defausser_btn.png"))
        cls.__boutonDefausse.position = Vec2(-50, 8)
        cls.__boutonDefausse.taille = Vec2(20, 10)

        def make_callback_d():
            def callback(btn: Bouton):
                cls.__gameManagerRef.btn_pressed = DEFAUSSE_BTN

            return callback

        cls.__boutonDefausse.ajouter_callback(make_callback_d())

        # Bouton Rester
        cls.__boutonRester = Bouton(join("assets", "rester_button.png"))
        cls.__boutonRester.position = Vec2(50, 8)
        cls.__boutonRester.taille = Vec2(20, 10)

        def make_callback_r():
            def callback(btn: Bouton):
                cls.__gameManagerRef.manche.main.choix = "s"

            return callback

        cls.__boutonRester.ajouter_callback(make_callback_r())

        # Bouton Prendre
        cls.__boutonPrendre = Bouton(join("assets", "prendre_button.png"))
        cls.__boutonPrendre.position = Vec2(50, 22)
        cls.__boutonPrendre.taille = Vec2(20, 10)

        def make_callback_p():
            def callback(btn: Bouton):
                cls.__gameManagerRef.manche.main.choix = "p"

            return callback

        cls.__boutonPrendre.ajouter_callback(make_callback_p())

    @classmethod
    def setupSprite(cls, sprite: Sprite, idxJeu: int, idxCarte: int):
        offset = 0
        pos = Vec2(-54 + 25 * idxJeu, -20)
        if idxJeu in cls.__gameManagerRef.jeu_cibles:
            if idxJeu == cls.__gameManagerRef.manche.main.jeu_en_cours:
                offset = 0
                pos = Vec2(-15, 15)
            else:
                offset = 5

        sprite.taille = 20

        if idxCarte == 0:
            sprite.rotation = radians(15)
            sprite.position = pos
        elif idxCarte == 1:
            sprite.rotation = radians(-15)
            sprite.position = Vec2(pos.x+7,pos.y)
        else:
            extra = idxCarte - 1
            sprite.rotation = radians(0)
            sprite.position = Vec2((pos.x+7)+ extra * 6,pos.y - extra * 3)

        sprite.position.y += offset

    @classmethod
    def draw_ui(cls):
        if cls.__spriteRendererRef is None:
            from src.core.application import Application
            cls.__spriteRendererRef = Application.get_instance().get_sprite_renderer()
        if cls.__gameManagerRef is None:
            from src.core.application import Application
            cls.__gameManagerRef = Application.get_instance().get_game_manager()

        cls.__draw_main_proposer()
        cls.__draw_texte()

    @classmethod
    def __draw_main_proposer(cls):
        jeux_proposes = cls.__gameManagerRef.manche.main.jeux
        for i in range(min(len(jeux_proposes), 5)):
            jeu = jeux_proposes[i]
            cartes = jeu.cartes

            for j, carte in enumerate(cartes):
                sprite = cls.get_card_sprite(carte.val, carte.cou)
                if sprite is not None:
                    cls.setupSprite(sprite, i, j)
                    cls.__spriteRendererRef.envoyer(sprite)

            cls.__draw_bouton_selection(i)

    @classmethod
    def __draw_bouton_selection(cls, idxJeu: int):
        pos = Vec2(-50 + 25 * idxJeu, -40)
        bouton = cls.__boutonSelection[idxJeu]
        bouton.taille = Vec2(16, 8)
        bouton.position = pos
        cls.__spriteRendererRef.envoyer(bouton)

    @classmethod
    def __draw_texte(cls):
        Texte.render_text(f"Mains restantes : {cls.__gameManagerRef.manche.nb_main}", -375, 250, 0.5, Vec3())
        Texte.render_text(f"Defausses restantes : {cls.__gameManagerRef.manche.nb_defausse}", -375, 225, 0.5, Vec3())
        Texte.render_text(f"Points : {cls.__gameManagerRef.manche.point}", -375, 275, 0.5, Vec3())
        if cls.__gameManagerRef.en_attente_choix:
            Texte.render_text("Choisissez Prendre ou Rester", -375, 200, 0.5, Vec3())

        cls.__spriteRendererRef.envoyer(cls.__boutonJouer)
        cls.__spriteRendererRef.envoyer(cls.__boutonDefausse)
        cls.__spriteRendererRef.envoyer(cls.__boutonPrendre)
        cls.__spriteRendererRef.envoyer(cls.__boutonRester)