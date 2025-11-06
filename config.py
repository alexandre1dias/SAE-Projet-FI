#>>>import random, string, os
#>>>"".join([random.choice(string.printable)for _in os.urandom(24)])
SECRET_KEY = "2lzUl{$*D6#`8uXqlU."

TITLE = "Cercle d'escrime Blois"
BOOTSTRAP_SERVE_LOCAL = True

LOGIN="kurucelik"
PASSWD="kurucelik"
SERVEUR="servinfo-maria"
BD="DBkurucelik"
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{LOGIN}:{PASSWD}@{SERVEUR}/{BD}'