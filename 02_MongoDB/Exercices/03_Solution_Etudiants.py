# -----------------------------------------------------------------------------------------
# EXERCICE 3 : GESTION DES ÉTUDIANTS (Correction)
# -----------------------------------------------------------------------------------------

import subprocess
import sys

# 1. VÉRIFICATION AUTOMATIQUE DE LA LIBRAIRIE
# Ce bloc permet d'installer 'pymongo' si vous ne l'avez pas encore fait manuellement.
try:
    import pymongo
except ImportError:
    print("Installation de la librairie 'pymongo'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pymongo"])
    print("Installation terminée.")
    import pymongo

from pymongo import MongoClient

# -----------------------------------------------------------------------------------------
# 2. CONNEXION
# -----------------------------------------------------------------------------------------
# C'est ici que l'on précise l'URL de connexion.
# Pour un serveur local par défaut, c'est toujours : mongodb://localhost:27017/
client = MongoClient("mongodb://localhost:27017/")

# Création (ou sélection) de la base de données 'universite'
db = client["universite"]

# Création (ou sélection) de la collection 'etudiants'
collection = db["etudiants"]

# Nettoyage (optionnel) : On vide la collection pour ne pas avoir de doublons si on relance le script
collection.delete_many({})
print("Base de données nettoyée pour l'exercice.\n")

# -----------------------------------------------------------------------------------------
# 3. INSERTION (CREATE)
# -----------------------------------------------------------------------------------------
print("--- Insertion des étudiants ---")

liste_etudiants = [
    {"nom": "Alice", "age": 20, "note": 14, "options": ["Math", "Physique"]},
    {"nom": "Bob", "age": 22, "note": 18, "options": ["Math", "Info"]},
    {"nom": "Charlie", "age": 19, "note": 10, "options": ["Anglais"]},
    {"nom": "David", "age": 21, "note": 19, "options": ["Info", "Physique"]}
]

collection.insert_many(liste_etudiants)
print("4 étudiants ajoutés avec succès.")

# -----------------------------------------------------------------------------------------
# 4. LECTURE (READ)
# -----------------------------------------------------------------------------------------
print("\n--- Recherche : Meilleurs étudiants (> 15/20) ---")

# On cherche les étudiants dont la "note" est "Greater Than" ($gt) 15
meilleurs = collection.find({"note": {"$gt": 15}})

for etudiant in meilleurs:
    print(f"- {etudiant['nom']} a eu {etudiant['note']}/20")

print("\n--- Recherche : Étudiants en Informatique ---")
# MongoDB est intelligent : si "options" est une liste, il vérifie si "Info" est DEDANS.
informaticiens = collection.find({"options": "Info"})

for etudiant in informaticiens:
    print(f"- {etudiant['nom']}")

# -----------------------------------------------------------------------------------------
# 5. MISE À JOUR (UPDATE)
# -----------------------------------------------------------------------------------------
print("\n--- Mise à jour : Alice progresse ---")

# On change la note d'Alice pour la passer à 16
collection.update_one(
    {"nom": "Alice"},           # Qui on modifie ?
    {"$set": {"note": 16}}      # Quoi on modifie ? ($set pour écraser la valeur)
)
print("La note d'Alice a été corrigée à 16.")

# -----------------------------------------------------------------------------------------
# 6. SUPPRESSION (DELETE)
# -----------------------------------------------------------------------------------------
print("\n--- Suppression : Départ de Charlie ---")

collection.delete_one({"nom": "Charlie"})
print("Charlie a été supprimé de la base.")

# -----------------------------------------------------------------------------------------
print("\n--- Exercice Terminé ! ---")
print("Allez voir dans MongoDB Compass :")
print("1. Actualisez les bases de données (bouton Reload en haut à gauche)")
print("2. Cherchez la base 'universite' -> collection 'etudiants'")
print("3. Vous devriez voir Alice (16/20), Bob et David. Charlie aura disparu.")
