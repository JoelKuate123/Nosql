# Module 2 : MongoDB - La Base de Données Document

## 1. Introduction à MongoDB

MongoDB est une base de données NoSQL orientée **documents**.
Au lieu de stocker des données dans des tables (lignes/colonnes) comme Excel ou SQL, elle les stocke dans des documents **JSON** (JavaScript Object Notation), regroupés dans des **collections**.

### Comparaison SQL vs MongoDB
| SQL (Relationnel) | MongoDB (NoSQL) | Description |
| :--- | :--- | :--- |
| Database | Database | Conteneur global des données |
| Table | **Collection** | Groupe de documents similaires (ex: `users`) |
| Row (Ligne) | **Document** | Une entrée de données (ex: `Alice`) |
| Column (Colonne) | **Field (Champ)** | Attribut d'un document (ex: `age`) |
| Join | **Embedding / $lookup** | Lier des données entre elles |

### Exemple de Document MongoDB
```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "nom": "Dupont",
  "prenom": "Jean",
  "age": 30,
  "adresse": {
    "rue": "10 rue de la Paix",
    "ville": "Paris",
    "cp": "75000"
  },
  "hobbies": ["football", "lecture", "cinéma"]
}
```
*Notez que l'adresse est imbriquée dans le document, et les hobbies sont une liste.*

---

## 2. Installation et Démarrage

### Installation (Windows / Mac / Linux)
Le plus simple est d'utiliser Docker ou d'installer la version Community Server depuis le site officiel de MongoDB.

Commandes de base (Terminal) :
```bash
# Vérifier si MongoDB tourne
mongod --version

# Démarrer le serveur (si installation manuelle)
mongod

# Se connecter au Shell MongoDB (le client)
mongosh
```

---

## 3. Opérations CRUD (Create, Read, Update, Delete)

Une fois connecté avec `mongosh` ou via un pilote (comme Python), voici les commandes essentielles.
On utilisera la base de données `ecommerce`.

```javascript
use ecommerce  // Crée la base si elle n'existe pas
```

### C - Create (Insérer)
```javascript
// Insérer un seul produit
db.produits.insertOne({
  nom: "iPhone 15",
  prix: 999,
  categorie: "Smartphone",
  stock: 50
})

// Insérer plusieurs produits
db.produits.insertMany([
  { nom: "Samsung S23", prix: 899, categorie: "Smartphone" },
  { nom: "MacBook Air", prix: 1299, categorie: "Laptop" }
])
```

### R - Read (Lire)
```javascript
// Tout afficher
db.produits.find()

// Filtrer (équivalent WHERE)
db.produits.find({ categorie: "Smartphone" })

// Filtrer avec opérateur (Prix > 1000)
db.produits.find({ prix: { $gt: 1000 } })

// Lire un seul document (le premier trouvé)
db.produits.findOne({ nom: "iPhone 15" })
```

### U - Update (Modifier)
```javascript
// Mettre à jour un produit (modifier le prix)
db.produits.updateOne(
  { nom: "iPhone 15" },      // Filtre (Qui ?)
  { $set: { prix: 949 } }    // Action (Quoi ?)
)

// Incrémenter une valeur (ajouter 10 au stock de tous les Smartphones)
db.produits.updateMany(
  { categorie: "Smartphone" },
  { $inc: { stock: 10 } }
)
```

### D - Delete (Supprimer)
```javascript
// Supprimer un produit spécifique
db.produits.deleteOne({ nom: "Samsung S23" })

// Supprimer tous les Laptops
db.produits.deleteMany({ categorie: "Laptop" })
```

---

## 4. L'Aggregation Framework (Analyses Avancées)

L'agrégation est l'outil le plus puissant de MongoDB. C'est un **pipeline** : les données entrent d'un côté, subissent des transformations (étapes), et ressortent de l'autre.
C'est l'équivalent des `GROUP BY`, `SUM`, `AVG`, `JOIN` en SQL.

### Exemple : Chiffre d'affaires par catégorie
Imaginons une collection `ventes`.

```javascript
db.ventes.aggregate([
  // Étape 1 : $match (Filtrer) -> Garder uniquement les ventes "terminées"
  { $match: { statut: "terminé" } },

  // Étape 2 : $group (Grouper) -> Calculer le total par catégorie
  { $group: {
      _id: "$categorie",              // Grouper par ce champ
      totalVentes: { $sum: "$montant" }, // Somme des montants
      nombreVentes: { $sum: 1 }         // Compter les documents
    }
  },

  // Étape 3 : $sort (Trier) -> Du plus grand au plus petit chiffre d'affaires
  { $sort: { totalVentes: -1 } }
])
```

---

## 5. Bonnes Pratiques

1. **Modélisation** : En NoSQL, on modélise pour la **lecture**. Si vous affichez souvent un utilisateur AVEC ses dernières commandes, stockez les commandes DANS le document utilisateur (si peu nombreuses).
2. **Index** : Comme en SQL, créez des index sur les champs souvent recherchés (ex: email, nom) pour éviter que MongoDB scanne toute la collection.
   ```javascript
   db.utilisateurs.createIndex({ email: 1 })
   ```
3. **Sécurité** : Ne jamais exposer MongoDB directement sur internet (port 27017) sans authentification.
