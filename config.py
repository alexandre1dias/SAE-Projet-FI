#>>>import random, string, os
#>>>"".join([random.choice(string.printable)for _in os.urandom(24)])
from datetime import datetime
SECRET_KEY = "2lzUl{$*D6#`8uXqlU."

TITLE = "Cercle d'escrime Blois"
BOOTSTRAP_SERVE_LOCAL = True

LOGIN=""
PASSWD=""
SERVEUR="servinfo-maria"
BD=""
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{LOGIN}:{PASSWD}@{SERVEUR}/{BD}'

AUJOURDHUI = datetime.now().date()
LISTE_ANNEE=["2023-2024"]
ALLOWED_EXTENSIONS = {'webp','png', 'jpg', 'jpeg', 'gif'}
