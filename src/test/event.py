import threading
import time
from src.event.event import *
import unittest

class TestEventSystem(unittest.TestCase):
    def setUp(self):
        # remettre l'etat initial entre tests
        SystemEvenement._event_classes.clear()
        SystemEvenement._listeners.clear()

    def test_event_tache_effectuer_arriere_plan(self):
        @SystemEvenement.enregistrer_event
        class TestEvent:
            def __init__(self):
                pass

        executed = []

        @SystemEvenement.ecouter("TestEvent")
        def listener(event):
            executed.append("ok")

        start = time.time()
        SystemEvenement.envoyer(TestEvent())
        elapsed = time.time() - start

        # envoyer() ne doit pas bloquer
        self.assertLess(elapsed, 0.05)

        # attendre que le worker traite l'event
        timeout = time.time() + 1
        while not executed and time.time() < timeout:
            time.sleep(0.01)

        self.assertEqual(executed, ["ok"])


    def test_tout_les_events_sont_executer(self):
        @SystemEvenement.enregistrer_event
        class TestEvent:
            def __init__(self, i):
                self.i = i
                

        results = []

        @SystemEvenement.ecouter("TestEvent")
        def listener(event):
            results.append(event.i)

        for i in range(5):
            SystemEvenement.envoyer(TestEvent(i))

        timeout = time.time() + 1
        while len(results) < 5 and time.time() < timeout:
            time.sleep(0.01)

        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])

    def test_listener_fonctionne_sur_autre_thread(self):
        @SystemEvenement.enregistrer_event
        class TestEvent:
            def __init__(self):
                pass

        calling_thread = threading.get_ident()
        listener_thread = None
        done = threading.Event()

        @SystemEvenement.ecouter("TestEvent")
        def listener(event):
            nonlocal listener_thread
            listener_thread = threading.get_ident()
            done.set()

        SystemEvenement.envoyer(TestEvent())

        self.assertTrue(done.wait(timeout=1))
        self.assertNotEqual(calling_thread, listener_thread)


if __name__ == '__main__':
    unittest.main()