
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, IntegerField, TextAreaField, DateTimeLocalField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    Login = StringField ('Email' ,validators= [DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    next = HiddenField()
    connecter = SubmitField()

class EventForm(FlaskForm):
    title = StringField('Titre de l\'événement', validators=[DataRequired()])
    start_date = DateTimeLocalField('Date et heure de début', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeLocalField('Date et heure de fin', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    category = SelectField('Catégorie', choices=[
        ('Entraînement', 'Entraînement'),
        ('Compétition', 'Compétition'),
        ('Réunion', 'Réunion'),
        ('Evenement du club', 'Evenement du club')
    ], validators=[DataRequired()])
    level = SelectMultipleField('Niveaux concernés', choices=[
        ('M9', 'M9'),
        ('M11', 'M11'),
        ('M13', 'M13'),
        ('M15', 'M15'),
        ('M17', 'M17'),
        ('M20', 'M20'),
        ('Senior', 'Senior'),
        ('Veteran', 'Veteran')
    ], validators=[DataRequired()])
    description = TextAreaField('Description (optionnel)')
    submit = SubmitField('Ajouter l\'événement')
 

class ParametresForm(FlaskForm):
    nom = StringField('Nom', validators=[Optional()])
    prenom = StringField('Prenom', validators=[Optional()])
    age = IntegerField('age', validators=[Optional()])
    date = StringField('nouvelle date de naissance', validators=[Optional()])
    categorie = StringField('Categorie', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Nouveau mot de passe', validators=[Optional()])
    submit = SubmitField('Envoyer la requête')