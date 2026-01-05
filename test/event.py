import threading
import time
from src.event.event import *
import unittest

class TestEventSystem(unittest.TestCase):
    def setUp(self):
        # Remettre l'etat initial entre tests
        EventSystem._event_classes.clear()
        EventSystem._listeners.clear()

    def test_creer_evenement_inexistant(self):
        e = EventSystem.creer_evenement("inexistant", a=1, b=2)
        self.assertEqual(e.a, 1)
        self.assertEqual(e.b, 2)
        self.assertFalse(e.handled)

    def test_enregistrer_event_et_creation_instance(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self, x=0):
                self.x = x
                self.handled = False

        e = EventSystem.creer_evenement("TestEvent", x=5)
        self.assertIsInstance(e, TestEvent)
        self.assertEqual(e.x, 5)

    def test_handled_arrete_propagation(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self):
                self.handled = False

        # nettoyer les ecouteurs pour TestEvent
        EventSystem._listeners.pop("TestEvent", None)

        events = []
        def first(e):
            events.append('first')
            e.handled = True
        def second(e):
            events.append('second')

        # enregistrer manuellement des listeners sans utiliser le decorateur
        EventSystem._listeners.setdefault("TestEvent", []).append({
            "function": first,
            "priorite": 1,
            "original": first
        })
        EventSystem._listeners["TestEvent"].append({
            "function": second,
            "priorite": 0,
            "original": second
        })

        EventSystem.envoyer(EventSystem.creer_evenement("TestEvent"))
        self.assertEqual(events, ['first'])

    def test_listener_verifier_prioriter(self):
        # regarde si le systeme de priorité fonctionne
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self):
                self.handled = False

        order = []

        @EventSystem.listener("TestEvent", priority=1)
        def high(e):
            order.append('high')

        @EventSystem.listener("TestEvent", priority=0)
        def low(e):
            order.append('low')

        EventSystem.envoyer(EventSystem.creer_evenement("TestEvent"))
        self.assertEqual(order, ['high', 'low'])

    def test_event_tache_effectuer_arriere_plan(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self):
                self.handled = False

        executed = []

        @EventSystem.listener("TestEvent")
        def listener(event):
            executed.append("ok")

        start = time.time()
        EventSystem.envoyer(TestEvent())
        elapsed = time.time() - start

        # envoyer() ne doit pas bloquer
        self.assertLess(elapsed, 0.05)

        # attendre que le worker traite l'event
        timeout = time.time() + 1
        while not executed and time.time() < timeout:
            time.sleep(0.01)

        self.assertEqual(executed, ["ok"])

    def test_handled_arrete_autre_listener(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self):
                self.handled = False

        calls = []

        @EventSystem.listener("TestEvent", priority=1)
        def first(event):
            calls.append("first")
            event.handled = True

        @EventSystem.listener("TestEvent", priority=0)
        def second(event):
            calls.append("second")

        EventSystem.envoyer(TestEvent())

        timeout = time.time() + 1
        while not calls and time.time() < timeout:
            time.sleep(0.01)

        self.assertEqual(calls, ["first"])

    def test_tout_les_events_sont_executer(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self, i):
                self.i = i
                self.handled = False

        results = []

        @EventSystem.listener("TestEvent")
        def listener(event):
            results.append(event.i)

        for i in range(5):
            EventSystem.envoyer(TestEvent(i))

        timeout = time.time() + 1
        while len(results) < 5 and time.time() < timeout:
            time.sleep(0.01)

        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])

    def test_listener_fonctionne_sur_autre_thread(self):
        @EventSystem.enregistrer_event
        class TestEvent:
            def __init__(self):
                self.handled = False

        calling_thread = threading.get_ident()
        listener_thread = None
        done = threading.Event()

        @EventSystem.listener("TestEvent")
        def listener(event):
            nonlocal listener_thread
            listener_thread = threading.get_ident()
            done.set()

        EventSystem.envoyer(TestEvent())

        self.assertTrue(done.wait(timeout=1))
        self.assertNotEqual(calling_thread, listener_thread)


if __name__ == '__main__':
    unittest.main()