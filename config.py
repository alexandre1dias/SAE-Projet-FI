#>>>import random, string, os
#>>>"".join([random.choice(string.printable)for _in os.urandom(24)])
SECRET_KEY = "2lzUl{$*D6#`8uXqlU."

TITLE = "Cercle d'escrime Blois"

import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'monApp.db')
BOOTSTRAP_SERVE_LOCAL = True