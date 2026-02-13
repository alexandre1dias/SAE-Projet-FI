import click
from .app import app, db
from .models import AdminBD
from werkzeug.security import generate_password_hash

@app.cli.command()
@click.argument('email')
@click.argument('new_password')
def change_admin_password(email, new_password):
    """Change le mot de passe d'un administrateur via le terminal."""
    
    # recherche de l'admin par son mail
    admin = AdminBD.query.filter_by(email=email).first()
    
    if admin:
        hash_mdp = generate_password_hash(new_password, method='pbkdf2:sha256')
        
        # mise à jour du champ mdp_hash 
        admin.mdp_hash = hash_mdp
        db.session.commit()
        
        print(f"Succès : Le mot de passe pour l'admin '{email}' a été mis à jour.")
    else:
        print(f"Erreur : Aucun administrateur trouvé avec l'email '{email}'.")