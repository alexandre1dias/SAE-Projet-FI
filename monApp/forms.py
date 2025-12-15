
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, IntegerField, TextAreaField, DateTimeLocalField, SelectField, SelectMultipleField, DateField, RadioField, widgets, MultipleFileField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from datetime import date
from flask_wtf.file import FileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField ('Email' ,validators= [DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    connecter = SubmitField('Se connecter')

class PasswordChangeForm(FlaskForm):
    old_password = PasswordField ('Ancien mot de passe', validators=[DataRequired()])
    new_password = PasswordField ('Nouveau mot de passe', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirmer le nouveau mot de passe', validators=[DataRequired()])
    next = HiddenField()
    submit = SubmitField('Valider la modification')

class ModifForm(FlaskForm):
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
        ('Membre du comité', 'Membre du comité'),
        ('Secrétaire Général', 'Secrétaire Général'),
        ('Trésorier Général', 'Trésorier Général'),
        ('Vice-président', 'Vice-président'),
        ('Président', 'Président')
    ], validators=[DataRequired()]) 
    justification = TextAreaField('Justification de la demande (optionnel)', validators=[Optional()])

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
        ('M9', 'M9'), ('M11', 'M11'), ('M13', 'M13'), ('M15', 'M15'),
        ('M17', 'M17'), ('M20', 'M20'), ('Senior', 'Senior'), ('Veteran', 'Veteran')
    ], 
    validators=[Optional()],
    widget=widgets.ListWidget(prefix_label=False),
    option_widget=widgets.CheckboxInput()
    ) 
    
    sexe = SelectField('Sexe concerné', choices=[
        ('Homme', 'Homme'), ('Femme', 'Femme')
    ], validators=[Optional()]) 
    
    arme = SelectField('Arme concernée', choices=[
        ('Fleuret', 'Fleuret'), ('Épée', 'Épée'), ('Sabre', 'Sabre')
    ], validators=[Optional()])
    
    type = SelectField('Type d\'événement', choices=[
        ('Regionale', 'Regionale'), ('National', 'National')
    ], validators=[Optional()])
    ville = StringField('Ville de l\'événement', validators=[DataRequired()])
    adresse = StringField('Adresse de l\'événement', validators=[DataRequired()])
    description = TextAreaField('Description (optionnel)')
    submit = SubmitField('Ajouter l\'événement')
    
    def validate_level(self, level):
        """
        Valide le champ 'level'.
        1. Vérifie s'il est requis pour la catégorie.
        2. Vérifie qu'il n'y a pas de niveaux consécutifs pour une compétition.
        """
        selected_category = self.category.data
        selected_levels_data = level.data
        if selected_category in ['Compétition', 'Entraînement', 'Evenement du club'] and not selected_levels_data:
            raise ValidationError('Le niveau est requis pour ce type d\'événement.')
        if selected_category == 'Compétition' and selected_levels_data:
            selected_levels = set(selected_levels_data)
            consecutive_pairs = [
                {'M9', 'M11'},
                {'M11', 'M13'},
                {'M13', 'M15'},
                {'M15', 'M17'},
                {'M17', 'M20'},
                {'M20', 'Senior'},
                {'Senior', 'Vétéran'}
            ]
            for pair in consecutive_pairs:
                if selected_levels.issuperset(pair):
                    friendly_pair = " et ".join(sorted(list(pair)))
                    raise ValidationError(f'Règle de surclassement : Les niveaux {friendly_pair} ne peuvent pas être sélectionnés ensemble.')

    def validate_sexe(self, sexe):
        if self.category.data == 'Compétition' and not sexe.data:
            raise ValidationError('Le sexe est requis pour une compétition.')

    def validate_arme(self, arme):
        if self.category.data in ['Compétition', 'Entraînement'] and not arme.data:
            raise ValidationError('L\'arme est requise pour ce type d\'événement.')

    def validate_type(self, type):
        if self.category.data == 'Compétition' and not type.data:
            raise ValidationError('Le type (Régional/National) est requis for une compétition.')

    def validate_ville(self, ville):
        if self.category.data in ['Compétition', 'Evenement du club'] and not ville.data:
            raise ValidationError('La ville est requise pour ce type d\'événement.')

    def validate_adresse(self, adresse):
        if self.category.data in ['Compétition', 'Evenement du club'] and not adresse.data:
            raise ValidationError('L\'adresse est requise pour ce type d\'événement.')
 

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

class HoraireForm(FlaskForm):
    jour = SelectField('Jour', choices=[
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'), ('Dimanche', 'Dimanche')
    ], validators=[DataRequired()])
    heure_debut = StringField('Heure de début (ex: 19h00)', validators=[DataRequired()])
    heure_fin = StringField('Heure de fin (ex: 21h15)', validators=[DataRequired()])
    activite = StringField('Activité (ex: Entraînement Épée)', validators=[DataRequired()])
    details = TextAreaField('Détails (ex: M17, M20...)', validators=[Optional()])
    submit = SubmitField('Enregistrer')

class TarifForm(FlaskForm):
    nom = StringField('Intitulé (ex: Initiation, Location annuelle)', validators=[DataRequired()])
    prix = IntegerField('Prix (€)', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    categorie = SelectField('Catégorie', choices=[
        ('Adhesion', 'Adhésion'),
        ('Materiel', 'Matériel')
    ], validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class InformationForm(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    contenu = TextAreaField('Contenu', validators=[DataRequired()])
    submit = SubmitField('Publier')

class ArticleForm(FlaskForm):
    titre = StringField('Titre de l\'article', validators=[DataRequired()])
    contenu = TextAreaField('Contenu complet', validators=[DataRequired()], render_kw={"rows": 10})
    images = MultipleFileField('Ajouter des photos', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images seulement !')
    ])
    submit = SubmitField('Publier l\'article')

class PresseForm(FlaskForm):
    titre = StringField('Titre de l\'article', validators=[DataRequired()])
    contenu = TextAreaField('Description / Contenu', validators=[DataRequired()], render_kw={"rows": 5})
    lien = StringField('Lien vers la source (URL)', validators=[DataRequired()])
    submit = SubmitField('Publier')