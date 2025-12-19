#>>>import random, string, os
#>>>"".join([random.choice(string.printable)for _in os.urandom(24)])
from datetime import datetime
SECRET_KEY = "2lzUl{$*D6#`8uXqlU."

TITLE = "Cercle d'escrime Blois"
BOOTSTRAP_SERVE_LOCAL = True

LOGIN=""
PASSWD=""
SERVEUR=""
BD=""
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{LOGIN}:{PASSWD}@{SERVEUR}/{BD}'

# exemple de configuration, on doit l'adapter mais vu qu'ici on a pas de serveur mail et qu'on fait le test sur le terminal ducoup pas besoin de vrai mail sender etc.
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_TLS = False
MAIL_USERNAME = None
MAIL_PASSWORD = None

AUJOURDHUI = datetime.now().date()
LISTE_ANNEE=["2023-2024"]