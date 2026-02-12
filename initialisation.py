import os
import subprocess
from lancement_bd import LancementBD
from lancement_venv import LancementVenv


class Initialisation():
    """
    Classe responsable de l'initialisation complète du projet, incluant la création
    de l'environnement virtuel, l'installation des dépendances, le déploiement de la
    base de données et le lancement de l'application Flask.
    """

    def __init__(self):
        self.lancement_bd = LancementBD()
        self.lancement_venv = LancementVenv()
        self.app_script = os.path.join("monApp", "app.py")

    def main(self):
        print("--- Initialisation du projet ---")
        self.lancement_venv.main()
        self.lancement_bd.main()
        #Lancement de Flask
        if os.path.exists(self.app_script):
            print(f"Lancement de l'application Flask via {self.app_script}...")
            try:
                subprocess.check_call([
                    self.lancement_venv.get_python_venv(), "-m", "flask",
                    "--app", self.app_script, "run"
                ])
            except KeyboardInterrupt:
                print("\nArrêt de l'application.")
        else:
            print(
                f"Fichier '{self.app_script}' introuvable. Impossible de lancer Flask."
            )


if __name__ == "__main__":
    initialisation = Initialisation()
    initialisation.main()
