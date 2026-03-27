import os

SCRIPT_DIR = os.path.dirname(__file__)

if not os.path.exists(os.path.join(SCRIPT_DIR,"src")):
    print("Dossier source introuvable")
    exit(1)
if not os.path.exists(os.path.join(SCRIPT_DIR,"assets")):
    print("Dossier assets introuvable")
    exit(1)

os.system("python -m src.main")