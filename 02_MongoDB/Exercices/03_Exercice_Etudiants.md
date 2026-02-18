# Exercice 3 : Gestion d'une base de données "Étudiants"

## Objectif
Créer un script Python pour gérer les notes des étudiants d'une université.
Vous apprendrez à créer une nouvelle base de données, insérer des documents complexes, et faire des recherches ciblées.

## Énoncé

1.  **Connexion** : Connectez-vous à votre serveur MongoDB local (`localhost:27017`).
2.  **Création** : Créez une base de données nommée `universite` et une collection `etudiants`.
3.  **Insertion** : Ajoutez les étudiants suivants :
    -   *Alice*, 20 ans, note: 14, options: Math, Physique
    -   *Bob*, 22 ans, note: 18, options: Math, Info
    -   *Charlie*, 19 ans, note: 10, options: Anglais
    -   *David*, 21 ans, note: 19, options: Info, Physique
4.  **Lecture (Recherche)** :
    -   Affichez tous les étudiants qui ont une note supérieure à 15.
    -   Affichez les étudiants qui suivent l'option "Info".
5.  **Mise à jour** : Alice a travaillé dur, augmentez sa note à 16.
6.  **Suppression** : L'étudiant "Charlie" quitte l'université, supprimez-le de la base.

---

## Résultat attendu dans MongoDB Compass

Une fois le script exécuté, ouvrez MongoDB Compass et actualisez (bouton vert en haut à gauche).

1.  Vous verrez apparaître une nouvelle base de données : **universite**.
2.  Dedans, une collection : **etudiants**.
3.  Si vous cliquez sur `etudiants`, vous devriez voir 3 documents (Charlie a été supprimé) :

**Document 1 : Alice (Note mise à jour)**
```json
{
  "_id": "...",
  "nom": "Alice",
  "age": 20,
  "note": 16,
  "options": ["Math", "Physique"]
}
```

**Document 2 : Bob**
```json
{
  "_id": "...",
  "nom": "Bob",
  "age": 22,
  "note": 18,
  "options": ["Math", "Info"]
}
```

**Document 3 : David**
```json
{
  "_id": "...",
  "nom": "David",
  "age": 21,
  "note": 19,
  "options": ["Info", "Physique"]
}
```
