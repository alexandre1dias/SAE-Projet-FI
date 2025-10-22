
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
    sexe = SelectField('Sexe concerné', choices=[
        ('Masculin', 'Masculin'),
        ('Féminin', 'Féminin'),
        ('Mixte', 'Mixte')
    ], validators=[DataRequired()])
    arme = SelectField('Arme concernée', choices=[
        ('Fleuret', 'Fleuret'),
        ('Épée', 'Épée'),
        ('Sabre', 'Sabre')
    ], validators=[DataRequired()])
    type = SelectField('Type d\'événement', choices=[
        ('Regionale', 'Regionale'),
        ('National', 'National')
    ], validators=[DataRequired()])
    description = TextAreaField('Description (optionnel)')
    submit = SubmitField('Ajouter l\'événement')
 

class ParametresForm(FlaskForm):
    nom = StringField('Nom', validators=[Optional()], render_kw={'readonly': True})
    prenom = StringField('Prenom', validators=[Optional()], render_kw={'readonly': True})
    age = StringField('age', validators=[Optional()], render_kw={'readonly': True})
    date = StringField('nouvelle date de naissance', validators=[Optional()], render_kw={'readonly': True})
    categorie = StringField('Categorie', validators=[Optional()], render_kw={'readonly': True})
    email = StringField('Email', validators=[Optional(), Email()], render_kw={'readonly': True})
    password = PasswordField('Nouveau mot de passe', validators=[Optional()], render_kw={'readonly': True})
    submit = SubmitField('Envoyer la requête')

class Parametres_updateForm(FlaskForm):
    nom = StringField('Nom', validators=[Optional()])
    prenom = StringField('Prenom', validators=[Optional()])
    age = IntegerField('age', validators=[Optional()])
    date = StringField('nouvelle date de naissance', validators=[Optional()])
    categorie = StringField('Categorie', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    password = PasswordField('Nouveau mot de passe', validators=[Optional()])
    submit = SubmitField('Envoyer la requête')