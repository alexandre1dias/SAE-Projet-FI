from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    Login = StringField ('Email' ,validators= [DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    next = HiddenField()
    connecter = SubmitField()
 
