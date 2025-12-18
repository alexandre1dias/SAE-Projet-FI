
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SubmitField, IntegerField, TextAreaField, DateTimeLocalField, SelectField, SelectMultipleField, DateField, RadioField, widgets, MultipleFileField
from wtforms.validators import DataRequired, Email, Optional, ValidationError
from datetime import date
from flask_wtf.file import FileField, FileAllowed
import phonenumbers

class LoginForm(FlaskForm):
    email = StringField ('Email' ,validators= [DataRequired(), Email()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    connecter = SubmitField('Se connecter')

class MdpOublieForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Envoyer')

class MdpChangeForm(FlaskForm):
    old_password = PasswordField ('Ancien mot de passe', validators=[DataRequired()])
    new_password = PasswordField ('Nouveau mot de passe', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirmer le nouveau mot de passe', validators=[DataRequired()])
    next = HiddenField()
    submit = SubmitField('Valider la modification')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nouveau mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le nouveau mot de passe', validators=[DataRequired()])
    submit = SubmitField('Réinitialiser le mot de passe')

    def validate_confirm_password(self, confirm_password):
        if self.password.data != confirm_password.data:
            raise ValidationError('Les mots de passe ne correspondent pas.')

class ModifForm(FlaskForm):
    nom = StringField ('nom' ,validators= [DataRequired()])
    prenom = StringField ('prenom' ,validators= [DataRequired()])
    ddn = StringField ('date de naissance' ,validators= [DataRequired()])
    sexe = SelectField('Sexe concerné', choices=[
        ('Homme', 'Homme'),
        ('Femme', 'Femme')
    ], validators=[DataRequired()])
    email = StringField ('Email' ,validators= [DataRequired(), Email()])
    numTel = StringField('Numéro de téléphone (optionnel)', validators=[Optional()])
    statut = SelectField('Statut', choices=[
        ('Membre', 'Membre'),
        ('Membre du comité', 'Membre du comité'),
        ('Secrétaire Général', 'Secrétaire Général'),
        ('Trésorier Général', 'Trésorier Général'),
        ('Vice-président', 'Vice-président'),
        ('Président', 'Président')
    ], validators=[DataRequired()]) 
    justification = TextAreaField('Justification de la demande (optionnel)', validators=[Optional()])

    def validate_numTel(self, field):
        if field.data:
            try:
                phone = phonenumbers.parse(field.data, "FR")
                if not phonenumbers.is_valid_number(phone):
                    raise ValidationError('Numéro de téléphone invalide.')
                # conversion au format INTERNATIONAL pour stockage String (ex: +33 6 12 34 56 78)
                field.data = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            except phonenumbers.NumberParseException:
                raise ValidationError('Numéro de téléphone invalide.')

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
    numTel = StringField('Numéro de téléphone (optionnel)', validators=[Optional()])
    password = PasswordField ('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField ('Confirmer mot de passe', validators=[DataRequired()])
    next = HiddenField()
    inscription = SubmitField()

    def validate_numTel(self, field):
        if field.data:
            try:
                phone = phonenumbers.parse(field.data, "FR")
                if not phonenumbers.is_valid_number(phone):
                    raise ValidationError('Numéro de téléphone invalide.')
                # conversion au format INTERNATIONAL pour stockage String (ex: +33 6 12 34 56 78)
                field.data = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            except phonenumbers.NumberParseException:
                raise ValidationError('Numéro de téléphone invalide.')

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
    validators=[],
    widget=widgets.ListWidget(prefix_label=False),
    option_widget=widgets.CheckboxInput()
    ) 
    type_reunion = StringField('Type de réunion', validators=[])
    sexe = SelectField('Sexe concerné', choices=[
        ('Homme', 'Homme'), ('Femme', 'Femme')
    ], validators=[]) 
    
    arme = SelectField('Arme concernée', choices=[
        ('Fleuret', 'Fleuret'), ('Épée', 'Épée'), ('Sabre', 'Sabre')
    ], validators=[])
    
    type = SelectField('Type d\'événement', choices=[
        ('Regionale', 'Regionale'), ('National', 'National')
    ], validators=[])
    ville = StringField('Ville de l\'événement', validators=[])
    adresse = StringField('Adresse de l\'événement', validators=[])
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


class FiltreForm(FlaskForm):
    CHOIX_SEXE = [('Homme', 'Homme'), ('Femme', 'Femme')]
    CHOIX_NIVEAU = [('M9', 'M9'), ('M11', 'M11'), ('M13', 'M13'), ('M15', 'M15'), 
                    ('M17', 'M17'), ('M20', 'M20'), ('Senior', 'Senior'), ('Vétéran', 'Vétéran')]
    CHOIX_FORMULAIRE = [('Question', 'Questions'), ('Demande', 'Demandes'), ('Signalement', 'Signalements')]
    CHOIX_ARMES = [('Sabre', 'Sabre'), ('Fleuret', 'Fleuret'), ('Épée', 'Épée')]
    CHOIX_TYPE_COMPETE = [('Régional', 'Régional'), ('National', 'National')]
    CHOIX_TYPE_EVENT = [('Compétition', 'Compétition'), ('Réunion', 'Réunion'),('Évènement du club', 'Évènement du club'), ('Entraînement', 'Entraînement')]


    sexe = SelectMultipleField(
        'Sexes',
        choices=CHOIX_SEXE,
        default=[c[0] for c in CHOIX_SEXE], 
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )
    
    niveau = SelectMultipleField(
        'Niveaux',
        choices=CHOIX_NIVEAU,
        default=[c[0] for c in CHOIX_NIVEAU],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    type_formulaire = SelectMultipleField(
        'Type',
        choices=CHOIX_FORMULAIRE,
        default=[c[0] for c in CHOIX_FORMULAIRE],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    armes = SelectMultipleField(
        'Armes',
        choices=CHOIX_ARMES,
        default=[c[0] for c in CHOIX_ARMES],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    type_competition = SelectMultipleField(
        'Type Competition',
        choices=CHOIX_TYPE_COMPETE,
        default=[c[0] for c in CHOIX_TYPE_COMPETE],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    type_event = SelectMultipleField(
        'Type Evenement',
        choices=CHOIX_TYPE_EVENT,
        default=[c[0] for c in CHOIX_TYPE_EVENT],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )

    recherche = StringField('Rechercher')
    submit = SubmitField('Envoyer')

    CHOIX_TRI = [('date_desc', 'Plus récent'), ('date_asc', 'Plus ancien')]
    tri = SelectField(
        'Trier par',
        choices=CHOIX_TRI,
        default='date_desc'  
    )

    
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
