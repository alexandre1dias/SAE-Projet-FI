# SAE-Projet-FI

Groupe composé de: Desgranges Lucas, Dias Alexandre, Kurucelik Erman, Schmit Clément

## Instruction pour lancer le projet
### Les prerequis:
Le projet necessite plusieurs frameworks
Pour pouvoir les installer, il faut d'abord crée un environnment venv.
Normalement, si vous avez python vous pouvez simplement creer votre environnement avec la commande:
* python -m venv venv
Ensuite lance votre venv avec la commande:
* source venv/bin/activate
Faite bien attention à mettre le bon chemin, ici par exemple, il est dans le dossier courant.

Une fois le venv installer, il vous faut installer tout les framework avec la commande
* pip install -r requirement.txt

### Les configs
Maintenant que tout est installer, il faut configurer les accès à la bd dans deux fichier: 
* config.py à la racine du projet
* db_config.conf dans le dossier BDD
Dans chacun d'eux, vous devez rentrer les informations de votre BD, exemple:
LOGIN="john"
PASSWD="doe"
SERVEUR="servinfo-maria"
BD="MaBD"

### Lancer le site
Une fois tout cela fait, vous pouvez lancer le site avec la commande 
* flask run
Attention, veillez bien à être dans le venv pour la faire.


