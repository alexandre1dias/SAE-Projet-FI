from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, FloatField, IntegerField, PasswordField
from wtforms.validators import DataRequired
from . models import User, Auteur
from hashlib import sha256
from monApp import db

class FormAuteur(FlaskForm):
    idA=HiddenField('idA')
    Nom = StringField ('Nom', validators =[DataRequired()])

class FormLivre(FlaskForm):
    idL=HiddenField("idL")
    Prix = FloatField ('Prix', validators =[DataRequired()])
    Titre = StringField("Titre", validators =[DataRequired()])
    Url = StringField("Url")
    Img = StringField("Img")
    auteur_id = IntegerField("auteur_id")


class LoginForm(FlaskForm):
    Login = StringField ('Identifiant')
    Password = PasswordField ('Mot de passe')
    next = HiddenField()
    def get_authenticated_user(self):
        unUser = db.session.get(User, self.Login.data)
        if unUser is None:
            return None
        m = sha256 ()
        m.update(self.Password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.Password else None