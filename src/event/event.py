from typing import *
import functools

# TODO: Ajouter une class Event pour faire l'enregistrement plus simplement
# TODO: Ajouter une File qui stoque les evenements et un "worker" qui va tout executer jusqu'a ce qu'il n'y ai plus rien a faire
class EventSystem:
    _event_classes = {}
    _listeners = {}

    @classmethod
    def enregistrer_event(cls,event_class):
        """Decorateur de class pour enregistrer un nouvel evenement"""
        cls._event_classes[event_class.__name__] = event_class
        return event_class

    @classmethod
    def listener(cls,event_type:str,priority:int=0):
        """Decorateur de fonction pour ajouter une fonction qui sera appeler quand un evenement sera lancer"""
        def decorator(func:Callable):
            @functools.wraps(func)
            def wrapper(event):
                return func(event)

            if event_type not in cls._listeners:
                cls._listeners[event_type] = []

            cls._listeners[event_type].append({
                "function": wrapper,
                "priority": priority,
                "original": func # Fonction original
            })

            # Trier pour avoir par prioriter
            cls._listeners[event_type].sort(key=lambda x:x["priority"],reverse=True)

            return wrapper
        return decorator

    @classmethod
    def envoyer(cls,event):
        """Executer toute les fonctions qui sont associer a l'evenement"""
        event_type = event.__class__.__name__
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                # Si l'evenement est deja traiter
                if hasattr(event, "handled") and event.handled:
                    break
                listener["function"](event)


    @classmethod
    def creer_evenement(cls,event_name:str,**kwargs) -> Any:
        """Sert a créé un nouvel evenement, faire event_system.creer_evenement("MouseEvent",x=0,y=0) est comme faire MouseEvent(x=0,y=0)"""
        # Si l'evenement existe
        if event_name in cls._event_classes:
            return cls._event_classes[event_name](**kwargs)
        else:
            # creer un evenement generique
            print("Creation d'un evenement inconnue!")
            class Event:
                def __init__(self,**data):
                    self.__dict__.update(data)
                    self.handled = False
            return Event(**kwargs)