# Utilise une image Python légère
FROM python:3.11-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie d'abord les dépendances pour optimiser le cache
COPY requirement.txt .

# Installe les dépendances (pense à corriger l'orthographe en 'requirements.txt' si possible)
RUN pip install --no-cache-dir -r requirement.txt

# Copie tout le contenu du dossier actuel dans le conteneur
COPY . .

# Port par défaut pour Flask
EXPOSE 5000

# Commande de lancement (lance l'initialisation puis l'app)
# On part du principe que ton app se lance via un script ou flask run
CMD python initialisation.py && python lancement_bd.py && flask run --host=0.0.0.0