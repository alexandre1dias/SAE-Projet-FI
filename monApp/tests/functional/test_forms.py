import pytest
from datetime import date, datetime, timedelta
from werkzeug.datastructures import MultiDict
from monApp.forms import *
from monApp.models import *

# ==============================================================================
# 1. AUTHENTIFICATION (Validation pure & Logique)
# ==============================================================================

def test_login_form(app):
    """Test LoginForm : Validation simple."""
    with app.test_request_context():
        form = LoginForm(formdata=MultiDict({
            'email': 'test@test.com',
            'password': 'password123'
        }))
        assert form.validate() is True
        form_bad = LoginForm(formdata=MultiDict({'email': 'bad', 'password': ''}))
        assert form_bad.validate() is False

def test_mdp_oublie_form(app):
    """Test MdpOublieForm."""
    with app.test_request_context():
        form = MdpOublieForm(formdata=MultiDict({'email': 'valid@test.fr'}))
        assert form.validate() is True

def test_mdp_change_form(app):
    """Test MdpChangeForm."""
    with app.test_request_context():
        form = MdpChangeForm(formdata=MultiDict({
            'old_password': 'old',
            'new_password': 'new',
            'confirm_new_password': 'new'
        }))
        assert form.validate() is True

def test_reset_password_form(app):
    """Test ResetPasswordForm."""
    with app.test_request_context():
        # Cas valide
        form = ResetPasswordForm(formdata=MultiDict({
            'password': 'pass',
            'confirm_password': 'pass'
        }))
        assert form.validate() is True
        # Cas invalide
        form_bad = ResetPasswordForm(formdata=MultiDict({
            'password': 'pass',
            'confirm_password': 'other'
        }))
        assert form_bad.validate() is False
        assert 'Les mots de passe ne correspondent pas.' in form_bad.errors['confirm_password']

# ==============================================================================
# 2. GESTION UTILISATEUR (Inscription / Modif / Parametres)
# ==============================================================================

def test_inscription_form_age_et_mdp(app, db):
    """Test InscriptionForm -> Sauvegarde InscriptionBD."""
    with app.test_request_context():
        today = date.today()
        # 15 ans en arrière
        date_naissance_valid = today.replace(year=today.year - 15)
        form = InscriptionForm(formdata=MultiDict({
            'Login': 'new@user.fr',
            'nom': 'Dupont',
            'prenom': 'Jean',
            'date_naissance': date_naissance_valid.strftime('%Y-%m-%d'),
            'sexe': 'Homme',
            'password': 'secure',
            'confirm_password': 'secure'
        }))
        assert form.validate() is True
        # Sauvegarde
        new_inscription = InscriptionBD(
            email=form.Login.data,
            nom=form.nom.data,
            prenom=form.prenom.data,
            ddn=form.date_naissance.data,
            sexe=form.sexe.data,
            mdp_hash=form.password.data,
            date=date.today()
        )
        db.session.add(new_inscription)
        db.session.commit()
        # Vérification BD
        saved = InscriptionBD.query.filter_by(email='new@user.fr').first()
        assert saved is not None
        assert saved.nom == 'Dupont'

def test_modif_form(app, db):
    """Test ModifForm -> Sauvegarde ModifBD."""
    with app.test_request_context():
        # Membre existant
        m = MembreBD(email='m@test.fr', nom='M', prenom='P', date_inscription=date.today())
        db.session.add(m)
        db.session.commit()

        form = ModifForm(formdata=MultiDict({
            'nom': 'New',
            'prenom': 'Name',
            'ddn': '2000-01-01',
            'sexe': 'Femme',
            'email': 'new@mail.com',
            'statut': 'Membre',
            'justification': 'Rien'
        }))
        assert form.validate() is True
        # Conversion date
        ddn_obj = datetime.strptime(form.ddn.data, '%Y-%m-%d').date()
        modif = ModifBD(
            id_membre=m.id,
            nom=form.nom.data,
            prenom=form.prenom.data,
            ddn=ddn_obj,
            email=form.email.data,
            date=date.today()
        )
        db.session.add(modif)
        db.session.commit()
        assert ModifBD.query.filter_by(id_membre=m.id).first().nom == 'New'

def test_parametres_form(app):
    """Test ParametresForm (Lecture seule)."""
    with app.test_request_context():
        form = ParametresForm(formdata=MultiDict({}))
        assert form.validate() is True

def test_parametres_update_form(app):
    """Test Parametres_updateForm (Pas de BD ici, simple validation)."""
    with app.test_request_context():
        form = Parametres_updateForm(formdata=MultiDict({'age': 20}))
        assert form.validate() is True

# ==============================================================================
# 3. ÉVÉNEMENTS (Compétition, Règles métier)
# ==============================================================================

def test_event_form_competition_valide(app, db):
    """Test EventForm (Valide) -> Sauvegarde CompetitionBD."""
    with app.test_request_context():
        form = EventForm(formdata=MultiDict({
            'title': 'Grand Tournoi',
            'start_date': '2025-06-01T09:00',
            'end_date': '2025-06-01T18:00',
            'category': 'Compétition',
            'level': ['M15', 'M20'],
            'sexe': 'Homme',
            'arme': 'Fleuret',
            'type': 'Regionale',
            'ville': 'Paris',
            'adresse': 'Gymnase'
        }))
        assert form.validate() is True
        evt = EvenementBD()
        db.session.add(evt)
        db.session.flush()
        comp = CompetitionBD(
            id_event=evt.id,
            nom=form.title.data,
            date_debut=form.start_date.data.date(),
            type_arme=form.arme.data,
            niveaux=",".join(form.level.data)
        )
        db.session.add(comp)
        db.session.commit()
        assert CompetitionBD.query.filter_by(nom='Grand Tournoi').first().type_arme == 'Fleuret'

def test_event_form_regles_specifiques(app):
    """Test EventForm : Règles métier (Validation pure)."""
    with app.test_request_context():
        # 1. Ville manquante
        form = EventForm(formdata=MultiDict({
            'title': 'Test',
            'start_date': '2025-01-01T10:00',
            'end_date': '2025-01-01T12:00',
            'category': 'Compétition',
            'level': ['M15'],
            'sexe': 'Femme',
            'arme': 'Épée',
            'type': 'National'
        }))
        assert form.validate() is False
        assert 'La ville est requise pour ce type d\'événement.' in str(form.errors['ville'])

        # 2. Surclassement
        form_lvl = EventForm(formdata=MultiDict({
            'title': 'Test',
            'start_date': '2025-01-01T10:00',
            'end_date': '2025-01-01T12:00',
            'category': 'Compétition',
            'level': ['M11', 'M13'],
            'sexe': 'Homme', 'arme': 'Sabre', 'type': 'Regionale',
            'ville': 'Lyon', 'adresse': 'Rue'
        }))
        assert form_lvl.validate() is False
        assert 'Règle de surclassement' in str(form_lvl.errors['level'])

# ==============================================================================
# 4. AUTRES FORMULAIRES (CMS, Contact, Filtres)
# ==============================================================================

def test_contact_form(app, db):
    """Test ContactForm -> Sauvegarde FormulaireBD."""
    with app.test_request_context():
        form = ContactForm(formdata=MultiDict({
            'type_form': 'Question',
            'sujet': 'Sujet',
            'email': 'user@test.com',
            'description': 'Desc'
        }))
        assert form.validate() is True
        f = FormulaireBD(
            type=form.type_form.data,
            sujet=form.sujet.data,
            email=form.email.data,
            date=date.today()
        )
        db.session.add(f)
        db.session.commit()
        assert FormulaireBD.query.first().email == 'user@test.com'

def test_filtre_form(app):
    """Test FiltreForm."""
    with app.test_request_context():
        form = FiltreForm(formdata=MultiDict({'sexe': ['Homme']}))
        assert form.validate() is True

def test_horaire_form(app, db):
    """Test HoraireForm -> Sauvegarde HoraireBD."""
    with app.test_request_context():
        form = HoraireForm(formdata=MultiDict({
            'jour': 'Lundi',
            'heure_debut': '18h',
            'heure_fin': '20h',
            'activite': 'Escrime'
        }))
        assert form.validate() is True
        h = HoraireBD(jour=form.jour.data, activite=form.activite.data)
        db.session.add(h)
        db.session.commit()
        assert HoraireBD.query.first().activite == 'Escrime'

def test_tarif_form(app, db):
    """Test TarifForm -> Sauvegarde TarifBD."""
    with app.test_request_context():
        form = TarifForm(formdata=MultiDict({
            'nom': 'Licence',
            'prix': 100,
            'categorie': 'Adhesion'
        }))
        assert form.validate() is True
        t = TarifBD(nom=form.nom.data, prix=form.prix.data)
        db.session.add(t)
        db.session.commit()
        assert TarifBD.query.first().prix == 100

def test_information_form(app, db):
    """Test InformationForm -> Sauvegarde InformationBD."""
    with app.test_request_context():
        form = InformationForm(formdata=MultiDict({
            'titre': 'Info',
            'contenu': 'Contenu'
        }))
        assert form.validate() is True
        i = InformationBD(titreIN=form.titre.data, dateIN=date.today())
        db.session.add(i)
        db.session.commit()
        assert InformationBD.query.first().titreIN == 'Info'

def test_presse_form(app, db):
    """Test PresseForm -> Sauvegarde PresseBD."""
    with app.test_request_context():
        form = PresseForm(formdata=MultiDict({
            'titre': 'Article',
            'contenu': 'Contenu',
            'lien': 'http://lien.com'
        }))
        assert form.validate() is True
        p = PresseBD(titreP=form.titre.data, lienP=form.lien.data, dateP=date.today())
        db.session.add(p)
        db.session.commit()
        assert PresseBD.query.first().lienP == 'http://lien.com'

def test_article_form(app, db):
    """Test ArticleForm -> Sauvegarde ArticleBD."""
    with app.test_request_context():
        form = ArticleForm(formdata=MultiDict({
            'titre': 'Titre',
            'contenu': 'Contenu'
        }))
        assert form.validate() is True
        a = ArticleBD(titre=form.titre.data, contenu=form.contenu.data)
        db.session.add(a)
        db.session.commit()
        assert ArticleBD.query.first().titre == 'Titre'