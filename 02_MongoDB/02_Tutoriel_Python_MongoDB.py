# -----------------------------------------------------------------------------------------
# TUTORIEL MONGODB AVEC PYTHON (PYMONGO)
# -----------------------------------------------------------------------------------------
# Ce script est un guide pas à pas pour manipuler MongoDB avec Python.
# Prérequis :
# 1. Avoir MongoDB installé et lancé sur votre machine (ou utiliser un cluster Atlas).
# 2. Installer la librairie pymongo : pip install pymongo
# -----------------------------------------------------------------------------------------

# Importation de la librairie nécessaire pour communiquer avec MongoDB
import subprocess
import sys

# Vérification et installation automatique de pymongo
try:
    import pymongo
except ImportError:
    print("Installation de la librairie 'pymongo'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])
    print("Installation terminée.")
    import pymongo

from pymongo import MongoClient

# Affichage pour suivre le déroulement du script
print("--- Démarrage du Tutoriel MongoDB ---")

# -----------------------------------------------------------------------------------------
# 1. CONNEXION À LA BASE DE DONNÉES
# -----------------------------------------------------------------------------------------

# On se connecte au serveur MongoDB local (localhost) sur le port par défaut (27017).
# Si vous utilisez un mot de passe ou un serveur distant, remplacez l'URL.
client = MongoClient("mongodb://localhost:27017/")

# On vérifie la connexion en listant les bases de données existantes
print("Bases de données existantes :", client.list_database_names())

# On sélectionne la base de données de travail.
# Note : Elle ne sera réellement créée que lorsqu'on y insérera des données.
db = client["tuto_python_db"]
print("Connexion à la base 'tuto_python_db' réussie.")

# On sélectionne une collection (équivalent d'une table en SQL).
# Ici, nous allons gérer des "utilisateurs".
collection_utilisateurs = db["utilisateurs"]

# Pour repartir de zéro à chaque lancement du script, on vide la collection
collection_utilisateurs.delete_many({})
print("Collection 'utilisateurs' nettoyée.")

# -----------------------------------------------------------------------------------------
# 2. CREATE (Insertion de données)
# -----------------------------------------------------------------------------------------
print("\n--- 2. Insertion de données (CREATE) ---")

# Création d'un document (dictionnaire Python) représentant un utilisateur
nouvel_utilisateur = {
    "nom": "Dupont",
    "prenom": "Jean",
    "age": 30,
    "ville": "Paris",
    "interets": ["Python", "Data", "Cinéma"]
}

# Insertion d'un seul document avec insert_one
resultat = collection_utilisateurs.insert_one(nouvel_utilisateur)
print(f"Utilisateur inséré avec l'ID : {resultat.inserted_id}")

# Création d'une liste de plusieurs utilisateurs
liste_utilisateurs = [
    {"nom": "Martin", "prenom": "Sophie", "age": 25, "ville": "Lyon", "interets": ["Voyage"]},
    {"nom": "Bernard", "prenom": "Lucas", "age": 40, "ville": "Paris", "interets": ["Cuisine", "Tech"]},
    {"nom": "Petit", "prenom": "Julie", "age": 22, "ville": "Marseille", "interets": ["Sport"]}
]

# Insertion de plusieurs documents avec insert_many
resultat_multiple = collection_utilisateurs.insert_many(liste_utilisateurs)
print(f"{len(resultat_multiple.inserted_ids)} utilisateurs insérés.")

# -----------------------------------------------------------------------------------------
# 3. READ (Lecture de données)
# -----------------------------------------------------------------------------------------
print("\n--- 3. Lecture de données (READ) ---")

# Lire tous les documents de la collection
print("-> Liste de tous les utilisateurs :")
tous_les_users = collection_utilisateurs.find()
for user in tous_les_users:
    print(user)

# Lire un utilisateur spécifique (Filtrer par ville = Paris)
print("\n-> Utilisateurs habitant à Paris :")
users_paris = collection_utilisateurs.find({"ville": "Paris"})
for user in users_paris:
    print(f"- {user['prenom']} {user['nom']}")

# Lire avec une condition complexe (Age supérieur à 25 ans)
# $gt signifie "Greater Than" (Plus grand que)
print("\n-> Utilisateurs de plus de 25 ans :")
users_plus_25 = collection_utilisateurs.find({"age": {"$gt": 25}})
for user in users_plus_25:
    print(f"- {user['prenom']} ({user['age']} ans)")

# -----------------------------------------------------------------------------------------
# 4. UPDATE (Mise à jour de données)
# -----------------------------------------------------------------------------------------
print("\n--- 4. Mise à jour de données (UPDATE) ---")

# Modifier l'âge de "Jean Dupont" (le passer à 31 ans)
# update_one modifie le premier document qui correspond au filtre
collection_utilisateurs.update_one(
    {"nom": "Dupont"},           # Le filtre pour trouver le document
    {"$set": {"age": 31}}        # L'action ($set pour modifier une valeur)
)
print("Âge de Jean Dupont mis à jour à 31 ans.")

# Ajouter un intérêt "MongoDB" à tous les habitants de Paris
collection_utilisateurs.update_many(
    {"ville": "Paris"},          # Filtre
    {"$push": {"interets": "MongoDB"}} # $push ajoute un élément dans une liste
)
print("Intérêt 'MongoDB' ajouté pour les Parisiens.")

# Vérification
print("-> Parisiens après modification :")
for user in collection_utilisateurs.find({"ville": "Paris"}):
    print(user)

# -----------------------------------------------------------------------------------------
# 5. DELETE (Suppression de données)
# -----------------------------------------------------------------------------------------
print("\n--- 5. Suppression de données (DELETE) ---")

# Supprimer l'utilisateur "Julie Petit"
collection_utilisateurs.delete_one({"nom": "Petit"})
print("Utilisateur Julie Petit supprimé.")

# -----------------------------------------------------------------------------------------
# 6. AGGREGATION (Analyses avancées)
# -----------------------------------------------------------------------------------------
print("\n--- 6. Agrégation (Stats) ---")

# Calculer l'âge moyen par ville
pipeline = [
    # Étape 1 : On ne garde que ceux qui ont un âge (sécurité)
    {"$match": {"age": {"$exists": True}}},
    
    # Étape 2 : On groupe par ville et on calcule la moyenne d'âge
    {"$group": {
        "_id": "$ville",             # La clé de groupement
        "age_moyen": {"$avg": "$age"}, # Calcul de la moyenne
        "nombre": {"$sum": 1}        # Compte le nombre de personnes
    }},
    
    # Étape 3 : On trie par âge moyen décroissant
    {"$sort": {"age_moyen": -1}}
]

resultats_agg = collection_utilisateurs.aggregate(pipeline)

print("Statistiques par ville :")
for stat in resultats_agg:
    print(f"- {stat['_id']} : {stat['nombre']} habitant(s), âge moyen {stat['age_moyen']} ans")

print("\n--- Fin du Tutoriel ---")
