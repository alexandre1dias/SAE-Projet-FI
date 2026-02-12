#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from config import LOGIN, PASSWD, SERVEUR, BD


class LancementBD:
    """
    Classe responsable de l'initialisation de la base de données MariaDB.
    Elle exécute les scripts SQL de création, de triggers et d'insertion.
    """

    def __init__(self):
        #Définition de l"environnement pour passer le mot de passe de manière sécurisée
        self.env = os.environ.copy()
        self.env["MYSQL_PWD"] = PASSWD
        self.commande_mysql = ["mysql", "-h", SERVEUR, "-u", LOGIN]
        self.scripts = [
            "destructionBD.sql", "creationBD.sql", "triggersBD.sql",
            "insertionBD.sql"
        ]

    def main(self):
        print("--- Initialisation de la Base de Données ---")

        if LOGIN == "" or PASSWD == "" or SERVEUR == "" or BD == "":
            print(
                "Erreur : Il manque des informations dans le fichier config.py")
            sys.exit(1)

        for script in self.scripts:
            script_path = os.path.join("BDD", script)

            if not os.path.exists(script_path):
                print(
                    f"Attention : Fichier '{script_path}' introuvable. Ignoré.")
                sys.exit(1)
            print(f"Exécution de {script}...")
            try:
                with open(script_path, "r", encoding="utf-8") as f:
                    subprocess.run(self.commande_mysql + [BD],
                                   stdin=f,
                                   env=self.env,
                                   check=True)

            except subprocess.CalledProcessError:
                print(f"Erreur lors de l'exécution de {script}.")
                sys.exit(1)

        print("\n--- Base de données déployée avec succès ! ---")


if __name__ == "__main__":
    lancement = LancementBD()
    lancement.main()
