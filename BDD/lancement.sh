#!/bin/bash

# Script de déploiement de la base de données MariaDB
# Usage: ./deploy_db.sh [config_file]

set -e  # Arrêter le script en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fichier de configuration par défaut
CONFIG_FILE="${1:-db_config.conf}"

# Fonction pour afficher les messages
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERREUR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

# Vérifier si le fichier de configuration existe
if [ ! -f "$CONFIG_FILE" ]; then
    log_error "Le fichier de configuration '$CONFIG_FILE' n'existe pas."
    log_info "Création d'un fichier de configuration template..."
    
    cat > "$CONFIG_FILE" << 'EOF'
# Configuration de la base de données MariaDB
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
DB_NAME=nom_de_la_base
EOF
    
    log_warning "Veuillez éditer le fichier '$CONFIG_FILE' avec vos paramètres de connexion."
    exit 1
fi

# Charger la configuration
source "$CONFIG_FILE"

# Vérifier que les variables sont définies
if [ -z "$DB_HOST" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_NAME" ]; then
    log_error "Configuration incomplète. Vérifiez le fichier '$CONFIG_FILE'."
    exit 1
fi

# Définir le port par défaut si non spécifié
DB_PORT=${DB_PORT:-3306}

# Commande de base pour MariaDB
MYSQL_CMD="mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD"

log_info "========================================="
log_info "Déploiement de la base de données"
log_info "========================================="
log_info "Serveur: $DB_HOST:$DB_PORT"
log_info "Utilisateur: $DB_USER"
log_info "Base de données: $DB_NAME"
log_info "========================================="

# Tester la connexion
log_info "Test de connexion au serveur MariaDB..."
if ! $MYSQL_CMD -e "SELECT 1;" > /dev/null 2>&1; then
    log_error "Impossible de se connecter au serveur MariaDB."
    log_error "Vérifiez vos paramètres de connexion dans '$CONFIG_FILE'."
    exit 1
fi
log_info "Connexion réussie!"

# Créer la base de données si elle n'existe pas
log_info "Création de la base de données '$DB_NAME' si nécessaire..."
$MYSQL_CMD -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
log_info "Base de données prête."

# Fonction pour exécuter un fichier SQL
execute_sql_file() {
    local file=$1
    local description=$2
    
    if [ ! -f "$file" ]; then
        log_warning "Le fichier '$file' n'existe pas. Ignoré."
        return 1
    fi
    
    log_info "$description"
    log_info "Exécution de: $file"
    
    if $MYSQL_CMD $DB_NAME < "$file"; then
        log_info "✓ $file exécuté avec succès"
        return 0
    else
        log_error "✗ Erreur lors de l'exécution de $file"
        return 1
    fi
}

# Ordre d'exécution des fichiers SQL
log_info ""
log_info "========================================="
log_info "ÉTAPE 1: Destruction de la base existante"
log_info "========================================="
execute_sql_file "destructionBD.sql" "Suppression des tables existantes..."

log_info ""
log_info "========================================="
log_info "ÉTAPE 2: Création de la structure"
log_info "========================================="
execute_sql_file "creationBD.sql" "Création des tables..."

log_info ""
log_info "========================================="
log_info "ÉTAPE 3: Création des triggers"
log_info "========================================="
execute_sql_file "triggersBD.sql" "Création des triggers et événements..."

log_info ""
log_info "========================================="
log_info "ÉTAPE 4: Insertion des données"
log_info "========================================="
execute_sql_file "insertionBD.sql" "Insertion des données de test..."

log_info ""
log_info "========================================="
log_info "Déploiement terminé avec succès!"
log_info "========================================="

# Empêcher la fermeture automatique de la fenêtre
echo ""
read -p "Appuyez sur Entrée pour fermer cette fenêtre..." -r
