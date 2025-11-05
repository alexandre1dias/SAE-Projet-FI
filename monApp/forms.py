
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, IntegerField, TextAreaField, DateTimeLocalField, SelectField, SelectMultipleField, DateField, RadioField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from . modelBD import MembreBD, InscriptionBD
from datetime import date

class LoginForm(FlaskForm):
    email = StringField ('Email' ,validators= [DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    connecter = SubmitField('Se connecter')

class PasswordChangeForm(FlaskForm):
    Login = StringField ('Email' ,validators= [DataRequired(), Email()])
    old_password = PasswordField ('Ancient mot de passe', validators=[DataRequired()])
    new_password = PasswordField ('Nouveau mot de passe', validators=[DataRequired()])
    next = HiddenField()
    connecter = SubmitField()

class MembreForm(FlaskForm):
    nom = StringField ('nom' ,validators= [DataRequired()])
    prenom = StringField ('prenom' ,validators= [DataRequired()])
    ddn = StringField ('date de naissance' ,validators= [DataRequired()])
    sexe = SelectField('Sexe concerné', choices=[
        ('Homme', 'Homme'),
        ('Femme', 'Femme')
    ], validators=[DataRequired()])
    email = StringField ('Email' ,validators= [DataRequired(), Email()])
    statut = SelectField('Statut', choices=[
        ('Membre', 'Membre'),
        ('Secrétaire Général', 'Secrétaire Général'),
        ('Trésorier Général', 'Trésorier Général'),
        ('Vice-président', 'Vice-président'),
        ('Président', 'Président')
    ], validators=[DataRequired()])
    



class InscriptionForm(FlaskForm):
    # cette fonction permet de vérifier que l'utilisateur a au moins 8 ans
    def validate_age(form, field):
        """
        Vérification que l'utilisateur a au moins 8 ans.
        """
        if field.data:
            today = date.today()
            # Calcul de l'âge
            age = today.year - field.data.year - ((today.month, today.day) < (field.data.month, field.data.day))
            if age < 8:
                raise ValidationError()
            
     # cette fonction permet de vérifier que l'utilisateur a entré les même mot de passe
    def validate_confirm_password(self, confirm_password):
        """
        Vérifie si les mots de passe correspondent.
        """
        if self.password.data != confirm_password.data:
            # Ce message s'affichera sous le champ de confirmation
            raise ValidationError('Les mots de passe ne correspondent pas.')
        
    Login = StringField ('Email' ,validators= [DataRequired(), Email()])
    nom = StringField ('nom' ,validators= [DataRequired()])
    prenom = StringField ('prenom' ,validators= [DataRequired()])
    date_naissance = DateField ('date de naissance' , format='%Y-%m-%d', validators=[DataRequired(), validate_age])
    sexe = SelectField ('sexe' , choices=[('Homme', 'Homme'), ('Femme', 'Femme')], validators=[DataRequired()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField ('Confirmer mot de passe', validators=[DataRequired()])
    next = HiddenField()
    inscription = SubmitField()

class ContactForm(FlaskForm):
    type_form = RadioField('Type de formulaire', choices=[
        ('Question', 'Question'),
        ('Demande', 'Demande'),
        ('Signalement', 'Signalement')
        ], validators=[DataRequired()])
    sujet = StringField('Sujet', validators=[DataRequired()])
    email = StringField('Votre Email', validators=[DataRequired(), Email()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

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