import os
import subprocess
import sys
import platform
import shutil


def main():
    #Configuration
    venv_dir = "venv"
    req_file = "requirement.txt"
    db_script = os.path.join("BDD", "lancement.sh")
    app_script = os.path.join("monApp", "app.py")

    print("--- Initialisation du projet ---")

    #Création de l'environnement virtuel
    if not os.path.exists(venv_dir):
        print(f"Création du dossier '{venv_dir}'...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
            print("Environnement virtuel créé.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de la création du venv : {e}")
            sys.exit(1)
    else:
        print(f"Le dossier '{venv_dir}' existe déjà.")

    #On chercher le chemin de pip dans le venv
    if platform.system() == "Windows":
        pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
        python_venv = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        python_venv = os.path.join(venv_dir, "bin", "python")

    if not os.path.exists(pip_exe):
        print(f"Erreur critique : Impossible de trouver {pip_exe}")
        sys.exit(1)

    #Installation des dépendances
    if os.path.exists(req_file):
        print(f"Installation des dépendances depuis {req_file}...")
        try:
            #Mise à jour de pip (Au cas ou)
            subprocess.check_call(
                [python_venv, "-m", "pip", "install", "--upgrade", "pip"])
            #Installation du fichier requirements.txt
            subprocess.check_call(
                [python_venv, "-m", "pip", "install", "-r", req_file])
            print("\n>>> Installation terminée avec succès ! <<<")
        except subprocess.CalledProcessError:
            print("Erreur lors de l'installation des paquets.")
            sys.exit(1)
    else:
        print(
            f"Fichier '{req_file}' introuvable. Aucune dépendance installée.")

    #Création de la base de données
    if os.path.exists(db_script):
        print(f"Création de la base de données via {db_script}...")
        cwd = os.getcwd()
        db_dir = os.path.dirname(db_script)
        script_name = os.path.basename(db_script)

        bash_cmd = "bash"
        # Sur Windows, si 'bash' n'est pas dans le PATH, on cherche dans les dossiers standards de Git
        if platform.system() == "Windows" and shutil.which("bash") is None:
            possible_paths = [
                r"C:\Program Files\Git\bin\bash.exe",
                r"C:\Program Files (x86)\Git\bin\bash.exe",
                r"C:\Windows\System32\bash.exe"
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    bash_cmd = path
                    break
            else:
                print("Erreur critique : 'bash' est introuvable. Veuillez installer Git Bash ou l'ajouter au PATH pour exécuter le script BDD.")
                sys.exit(1)

        try:
            # On se place dans le dossier de la BD pour exécuter le script shell
            os.chdir(db_dir)
            # Utilisation de bash pour lancer le script .sh
            subprocess.check_call([bash_cmd, script_name])
            os.chdir(cwd)
            print("Base de données créée avec succès.")
        except subprocess.CalledProcessError:
            os.chdir(cwd)
            print("Erreur lors de la création de la base de données.")
            sys.exit(1)
    else:
        print(f"Script '{db_script}' introuvable. Étape ignorée.")

    #Lancement de Flask
    if os.path.exists(app_script):
        print(f"Lancement de l'application Flask via {app_script}...")
        try:
            subprocess.check_call([python_venv, "-m", "flask", "--app", app_script, "run"])
        except KeyboardInterrupt:
            print("\nArrêt de l'application.")
    else:
        print(f"Fichier '{app_script}' introuvable. Impossible de lancer Flask.")


if __name__ == "__main__":
    main()
