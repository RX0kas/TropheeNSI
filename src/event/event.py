from typing import Callable,Any
import functools
import queue
import threading

# TODO: Ajouter une class Event pour faire l'enregistrement plus simplement
class EventSystem:
    _event_classes = {}
    _listeners = {}
    _file = queue.Queue()
    _thread = None
    
    @classmethod
    def _worker(cls):
        while True:
            event = cls._file.get()
            # Si plus rien a faire
            if event is None:
                break
            
            cls._executer_event(event)
            
    @classmethod
    def _executer_event(cls,event):
        event_type = event.__class__.__name__
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                listener["function"](event)

    @classmethod
    def enregistrer_event(cls,event_class):
        """Decorateur de class pour enregistrer un nouvel evenement"""
        cls._event_classes[event_class.__name__] = event_class
        return event_class

    @classmethod
    def listener(cls,event_type:str):
        """Decorateur de fonction pour ajouter une fonction qui sera appeler quand un evenement sera lancer"""
        def decorator(func:Callable):
            # functools.wraps permet de garder les informations de la fonction et donc aider durant le debugage
            @functools.wraps(func)
            def wrapper(event):
                return func(event)

            if event_type not in cls._listeners:
                cls._listeners[event_type] = []

            cls._listeners[event_type].append({
                "function": wrapper,
                "original": func # Fonction original
            })
            
            return wrapper
        return decorator

    @classmethod
    def envoyer(cls,event):
        """Executer toute les fonctions qui sont associer a l'evenement"""
        if cls._thread is None:
            print("Creation thread EventSystem")
            # daemon veut dire que si le programme veut s'arreter on n'attend pas le thread
            cls._thread = threading.Thread(target=cls._worker,daemon=True).start()
        cls._file.put(event)