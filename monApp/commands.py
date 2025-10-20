import click, logging as lg
from .app import app, db
from hashlib import sha256

@app.cli.command()
@click.argument('filename') 
def loaddb(filename):
    '''Creates the tables and populates them with data.'''
    # A Faire


@app.cli.command()    
def syncdb():
    '''Creates all missing tables . '''
    db.create_all()
    lg.warning('Database synchronized!')


# A modifier
"""
@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newuser (login, pwd):
    '''Adds a new user'''
    m = sha256()
    m.update(pwd.encode())
    unUser = User(Login=login ,Password =m.hexdigest())
    db.session.add(unUser)
    db.session.commit()
    lg.warning('User ' + login + ' created!')

# A modifier
@app.cli.command()
@click.argument('login')
@click.argument('pwd')
def newpasswrd(login, pwd):
    '''Change user's password'''
    user = User.query.filter_by(Login=login).first()
    if not user:
        print(f"User '{login}' not found.")
        return
    m = sha256()
    m.update(pwd.encode())
    user.Password = m.hexdigest()
    db.session.commit()
    print(f"Password for user '{login}' has been updated.")
"""