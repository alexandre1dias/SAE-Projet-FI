from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField


class LoginForm(FlaskForm):
    Login = StringField ('Identifiant')
    Password = PasswordField ('Mot de passe')
    next = HiddenField()

 
