import os
import subprocess
import sys
import platform


class LancementVenv():
    """
    Classe responsable de la gestion de l'environnement virtuel (venv).
    Elle permet de créer le dossier venv si nécessaire et d'installer
    automatiquement les dépendances listées dans le fichier requirement.txt.
    """

    def __init__(self):
        self.venv_dir = "venv"
        self.req_file = "requirement.txt"
        self.python_venv = None

    def main(self):
        self.creation_venv()
        self.installation_dependances()

    def creation_venv(self):
        #Création de l'environnement virtuel
        if not os.path.exists(self.venv_dir):
            print(f"Création du dossier '{self.venv_dir}'...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "venv", self.venv_dir])
                print("Environnement virtuel créé.")
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de la création du venv : {e}")
                sys.exit(1)
        else:
            print(f"Le dossier '{self.venv_dir}' existe déjà.")

    def installation_dependances(self):
        #On chercher le chemin de pip dans le venv
        if platform.system() == "Windows":
            pip_exe = os.path.join(self.venv_dir, "Scripts", "pip.exe")
            self.python_venv = os.path.join(self.venv_dir, "Scripts",
                                            "python.exe")
        else:
            pip_exe = os.path.join(self.venv_dir, "bin", "pip")
            self.python_venv = os.path.join(self.venv_dir, "bin", "python")

        if not os.path.exists(pip_exe):
            print(f"Erreur critique : Impossible de trouver {pip_exe}")
            sys.exit(1)

        #Installation des dépendances
        if os.path.exists(self.req_file):
            print(f"Installation des dépendances depuis {self.req_file}...")
            try:
                #Mise à jour de pip (Au cas ou)
                subprocess.check_call([
                    self.python_venv, "-m", "pip", "install", "--upgrade", "pip"
                ])
                #Installation du fichier requirements.txt
                subprocess.check_call([
                    self.python_venv, "-m", "pip", "install", "-r",
                    self.req_file
                ])
                print("\n>>> Installation terminée avec succès ! <<<")
            except subprocess.CalledProcessError:
                print("Erreur lors de l'installation des paquets.")
                sys.exit(1)
        else:
            print(
                f"Fichier '{self.req_file}' introuvable. Aucune dépendance installée."
            )

    def get_python_venv(self):
        return self.python_venv


if __name__ == "__main__":
    lancement = LancementVenv()
    lancement.main()
