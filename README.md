# Cours Complet : Bases de Données NoSQL pour Débutants 🚀

Bienvenue dans ce cours pratique conçu pour vous initier au monde du Big Data et du NoSQL.
Ce cours est structuré pour vous emmener du niveau zéro jusqu'à la mise en place d'architectures utilisées par Netflix, Uber ou Facebook.

## 📂 Structure du Cours

Le cours est divisé en 4 modules progressifs :

1. **01_Introduction_NoSQL/** : 
   - Comprendre pourquoi SQL ne suffit plus.
   - Le Théorème CAP (Concept fondamental).

2. **02_MongoDB/** (Base de données Document) :
   - Installation et concepts.
   - Manipulation de données JSON (CRUD).
   - Analyser des ventes (Aggregation Framework).
   - *Projet : Gestion de bibliothèque.*

3. **03_Cassandra/** (Base de données Colonnes) :
   - Architecture Masterless et Haute Disponibilité.
   - Modélisation pour l'IoT et les Logs.
   - *Projet : Capteurs de température.*

4. **04_Redis/** (Base de données Clé-Valeur) :
   - Le cache en mémoire RAM.
   - Compteurs temps réel et files d'attente.
   - *Projet : Backend de réseau social.*

---

## 🛠️ Prérequis Techniques

Pour suivre ce cours, vous aurez besoin de :

1. **Python** (version 3.x installée).
2. **Les librairies Python** (à installer via terminal) :
   ```bash
   pip install pymongo cassandra-driver redis
   ```
3. **Docker Desktop** (Fortement recommandé) :
   - C'est le moyen le plus simple d'avoir MongoDB, Cassandra et Redis sur votre machine sans "polluer" votre système.
   - Commandes pour lancer les bases de données :
     ```bash
     # MongoDB
     docker run --name mongo-tuto -p 27017:27017 -d mongo

     # Cassandra (Attention connexion peut prendre 1-2 min)
     docker run --name cassandra-tuto -p 9042:9042 -d cassandra

     # Redis
     docker run --name redis-tuto -p 6379:6379 -d redis
     ```

---

## 🎓 Comment suivre ce cours ?

Je vous conseille cet ordre :

1. Lisez le fichier `.md` de cours théorique dans chaque dossier.
2. Ouvrez et lisez le script `Tutoriel_Python_....py`.
   - **Lisez bien les commentaires**, ils expliquent chaque ligne.
   - Exécutez le script pour voir le résultat.
3. Allez dans le dossier `Exercices`.
   - Lisez l'énoncé.
   - Essayez de résoudre l'exercice par vous-même dans un nouveau fichier Python.
4. Comparez votre solution avec le fichier `Solutions_....py`.

Bon apprentissage ! 🎯
