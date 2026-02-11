from datetime import datetime
SECRET_KEY = "2lzUl{$*D6#`8uXqlU." # Garde ta clé actuelle

TITLE = "Cercle d'escrime Blois"
BOOTSTRAP_SERVE_LOCAL = True

LOGIN="root"
PASSWD="root"
SERVEUR="db"
BD="escrime_db"
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{LOGIN}:{PASSWD}@{SERVEUR}/{BD}'

AUJOURDHUI = datetime.now().date()
LISTE_ANNEE=["2023-2024"]
ALLOWED_EXTENSIONS = {'webp','png', 'jpg', 'jpeg', 'gif'}