# -----------------------------------------------------------------------------------------
# CORRECTION EXERCICES MONGODB
# -----------------------------------------------------------------------------------------

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

# 1. Connexion
client = MongoClient("mongodb://localhost:27017/")
db = client["bibliotheque"]
collection_livres = db["livres"]
collection_emprunts = db["emprunts"]

# Nettoyage pour que le script soit ré-exécutable
collection_livres.delete_many({})
collection_emprunts.delete_many({})

print("--- Début de la correction ---")

# -----------------------------------------------------------------------------------------
# EXERCICE 1 : Insertion
# -----------------------------------------------------------------------------------------
print("\n--- Exercice 1 : Insertion ---")

livres = [
    {"titre": "Le Petit Prince", "auteur": "Saint-Exupéry", "annee": 1943, "genres": ["Conte", "Philosophie"], "disponible": True},
    {"titre": "1984", "auteur": "George Orwell", "annee": 1949, "genres": ["SF", "Dystopie"], "disponible": True},
    {"titre": "Harry Potter", "auteur": "J.K. Rowling", "annee": 1997, "genres": ["Fantastique", "Jeunesse"], "disponible": True},
    {"titre": "L'Étranger", "auteur": "Albert Camus", "annee": 1942, "genres": ["Roman", "Absurde"], "disponible": True},
    {"titre": "Da Vinci Code", "auteur": "Dan Brown", "annee": 2003, "genres": ["Thriller", "Policier"], "disponible": True}
]

collection_livres.insert_many(livres)
print("5 livres insérés.")

# -----------------------------------------------------------------------------------------
# EXERCICE 2 : Requêtes et Updates
# -----------------------------------------------------------------------------------------
print("\n--- Exercice 2 : Lecture et Update ---")

# 1. Livres de genre 'Roman'
# Note : MongoDB cherche si 'Roman' est PRÉSENT dans la liste 'genres'
print("-> Livres de genre 'Roman' :")
romans = collection_livres.find({"genres": "Roman"})
for livre in romans:
    print(f"- {livre['titre']}")

# 2. Publiés après 2000
print("\n-> Livres après 2000 :")
recents = collection_livres.find({"annee": {"$gt": 2000}})
for livre in recents:
    print(f"- {livre['titre']} ({livre['annee']})")

# 3. Emprunter 'Le Petit Prince'
collection_livres.update_one(
    {"titre": "Le Petit Prince"},
    {"$set": {"disponible": False}}
)
print("\n'Le Petit Prince' est maintenant indisponible.")

# 4. Ajouter 'Classique' aux livres d'avant 1950
collection_livres.update_many(
    {"annee": {"$lt": 1950}},
    {"$push": {"genres": "Classique"}}
)
print("Genre 'Classique' ajouté aux vieux livres.")

# -----------------------------------------------------------------------------------------
# EXERCICE 3 : Agrégation (Bonus)
# -----------------------------------------------------------------------------------------
print("\n--- Exercice 3 : Emprunts ---")

# On insère des emprunts fictifs
emprunts = [
    {"utilisateur": "Alice", "livre_titre": "1984"},
    {"utilisateur": "Bob", "livre_titre": "1984"},
    {"utilisateur": "Charlie", "livre_titre": "Harry Potter"},
    {"utilisateur": "Alice", "livre_titre": "Le Petit Prince"},
    {"utilisateur": "David", "livre_titre": "1984"}
]
collection_emprunts.insert_many(emprunts)
print("Emprunts insérés.")

# Trouver le livre le plus emprunté
pipeline = [
    # Groupe par titre de livre et compte les occurrences
    {"$group": {"_id": "$livre_titre", "total_emprunts": {"$sum": 1}}},
    # Trie par nombre d'emprunts décroissant
    {"$sort": {"total_emprunts": -1}},
    # Garde le premier
    {"$limit": 1}
]

top_livre = list(collection_emprunts.aggregate(pipeline))
if top_livre:
    gagnant = top_livre[0]
    print(f"\nLe livre le plus populaire est '{gagnant['_id']}' avec {gagnant['total_emprunts']} emprunts.")
