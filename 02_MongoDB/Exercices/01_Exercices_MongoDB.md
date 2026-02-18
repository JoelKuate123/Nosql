# Exercices Pratiques MongoDB

## Contexte : Gestion d'une Bibliothèque
Vous développez le backend d'une application pour une bibliothèque municipale.
Vous devez gérer des **livres** et des **emprunts**.

---

## Exercice 1 : Création et Insertion (Niveau Débutant)
1. Créez un script Python ou utilisez MongoDB Compass/Shell.
2. Créez une base de données nommée `bibliotheque`.
3. Insérez 5 documents dans une collection `livres`.
   Chaque livre doit avoir :
   - Un titre (`titre`) (String)
   - Un auteur (`auteur`) (String)
   - Une année de publication (`annee`) (Int)
   - Des genres (`genres`) (Liste de Strings, ex: ["Roman", "Policier"])
   - Un état (`disponible`) (Booléen, mettre `True` par défaut)

*Exemple de livre :*
```json
{
  "titre": "Le Petit Prince",
  "auteur": "Antoine de Saint-Exupéry",
  "annee": 1943,
  "genres": ["Conte", "Philosophie"],
  "disponible": true
}
```

---

## Exercice 2 : Requêtes et Mises à jour (Niveau Intermédiaire)
1. Affichez tous les livres de genre "Roman".
2. Affichez tous les livres publiés après l'an 2000.
3. Le livre "Le Petit Prince" vient d'être emprunté.
   - Écrivez une requête pour passer son champ `disponible` à `False`.
4. Ajoutez le genre "Classique" à tous les livres publiés avant 1950 (utilisez l'opérateur `$push` et `$lt`).

---

## Exercice 3 : Modélisation et Agrégation (Niveau Avancé)
1. Insérez une collection `emprunts` qui contient l'historique.
   Chaque emprunt lie un utilisateur à un livre :
   ```json
   {
     "utilisateur": "Alice",
     "livre_titre": "Le Petit Prince",
     "date_emprunt": "2023-10-01"
   }
   ```
2. (Bonus) Essayez de trouver quel est le livre le plus emprunté (nécessite d'insérer plusieurs emprunts).
   *Indice : Utilisez un pipeline d'agrégation avec `$group` sur le champ `livre_titre` et `$sum`.*

---
**La correction se trouve dans le fichier `02_Solutions_MongoDB.py`.**
Essayez de le faire sans regarder la solution !
