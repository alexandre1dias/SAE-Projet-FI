# SAE-Projet-FI

**Groupe composé de :** Desgranges Lucas, Dias Alexandre, Kurucelik Erman, Schmit Clément

---

## Instructions pour lancer le projet

Pour le lancement du projet, nous avons créé un fichier `initialisation.py` qui fait tout pour vous.

### Prérequis
- Python installé
- Remplir les informations de votre base de données dans le fichier `config.py`

**Exemple de configuration :**
```python
LOGIN = "john"
PASSWD = "doe"
SERVEUR = "servinfo-maria"
BD = "MaBD"
```

### Lancement automatique

Une fois la configuration effectuée, lancez la commande suivante dans un terminal ouvert à la racine du projet :

```bash
python3 initialisation.py
```

Ce script va :
- Créer un environnement virtuel (venv)
- Installer toutes les dépendances et frameworks répertoriés dans `requirement.txt`
- Créer la base de données selon les informations du fichier `config.py`
- Lancer le site web

Vous n'aurez plus qu'à cliquer sur le lien ou aller à l'adresse suivante dans votre navigateur :

```
http://127.0.0.1:5000
```

> ⚠️ **Attention :** Cette adresse est locale. Si vous avez déjà un programme qui tourne sur le port 5000, cela ne fonctionnera pas. Assurez-vous que le port 5000 est bien libre.

---

## Informations utiles

À la racine du projet, vous trouverez des fichiers de lancement. Ces fichiers sont appelés dans `initialisation.py`, mais ils peuvent vous permettre de recréer le venv ou la base de données indépendamment.

### Scripts disponibles

- **`lancement_bd.py`** : Sert à créer la base de données. Utile si vous avez détruit votre BD ou si vous voulez relancer la BD de base du site.
  ```bash
  python3 lancement_bd.py
  ```

- **`lancement_venv.py`** : Sert à créer l'environnement virtuel. Si vous avez supprimé votre venv, utilisez :
  ```bash
  python3 lancement_venv.py
  ```

---

## Lancement manuel

Si vous voulez effectuer les étapes manuellement ou si le script `initialisation.py` ne fonctionne pas, voici la procédure :

### 1. Créer l'environnement virtuel
```bash
python -m venv venv
```

### 2. Activer l'environnement virtuel
```bash
source venv/bin/activate
```
> Faites bien attention à mettre le bon chemin. Ici, par exemple, il est dans le dossier courant.

### 3. Installer les frameworks
```bash
pip install -r requirement.txt
```

### 4. Configuration

Complétez les informations de votre base de données dans le fichier `config.py` à la racine du projet.

**Exemple :**
```python
LOGIN = "john"
PASSWD = "doe"
SERVEUR = "servinfo-maria"
BD = "MaBD"
```

### 5. Lancer le site

Une fois tout configuré, lancez le site avec la commande :
```bash
flask run
```
> ⚠️ Veillez bien à être dans l'environnement virtuel (venv) pour exécuter cette commande.

---

