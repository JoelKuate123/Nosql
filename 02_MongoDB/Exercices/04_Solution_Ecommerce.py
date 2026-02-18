# Importation des bibliothèques nécessaires
import pymongo  # Bibliothèque principale pour interagir avec MongoDB
from pymongo import MongoClient  # Pour créer une connexion au serveur
import random  # Pour générer des données de test aléatoires
from datetime import datetime, timedelta  # Pour manipuler les dates (création de commandes)

# 1. Connexion au serveur MongoDB local (port par défaut 27017)
client = MongoClient('mongodb://localhost:27017/')

# 2. Création ou accès à la base de données nommée 'ecommerce_tp'
db = client['ecommerce_tp']

# Nettoyage : On supprime les collections existantes pour repartir à zéro à chaque exécution
db.products.drop()  # Supprime la collection des produits
db.customers.drop()  # Supprime la collection des clients
db.orders.drop()  # Supprime la collection des commandes

# --- Tâche 1 : Modélisation de données (Concepts) ---
# En MongoDB, on modélise souvent en pensant aux requêtes futures.
# Ici, on utilise des "références" (comme des clés étrangères) pour lier les commandes aux clients et produits.

"""
Structure type d'un Produit :
{
    "_id": ObjectId,      # Identifiant unique généré par MongoDB
    "name": str,          # Nom du produit
    "price": float,       # Prix actuel
    "category": str,      # Catégorie (Electronique, etc.)
    "stock": int,         # Quantité disponible
    "tags": list          # Mots-clés pour la recherche
}
"""

# --- Tâche 2 : Insertion de données de test ---

# Étape 1 : Création de 50 produits variés
categories = ["Electronique", "Vêtements", "Maison", "Sport", "Beauté"]
product_list = []  # Liste temporaire pour stocker les objets produits avant insertion

for i in range(1, 51):  # Boucle pour générer 50 produits
    category = random.choice(categories)  # Choisit une catégorie au hasard
    product = {
        "name": f"Produit {i}",  # Nom unique (Produit 1, Produit 2, ...)
        "price": round(random.uniform(10.0, 500.0), 2),  # Prix entre 10€ et 500€
        "category": category,
        "stock": random.randint(0, 100),  # Stock entre 0 et 100
        "tags": [category.lower(), f"tag{i}"]  # Tags : catégorie et un tag unique
    }
    product_list.append(product)  # Ajoute le produit à notre liste

# Insertion massive des 50 produits dans la collection 'products'
inserted_products = db.products.insert_many(product_list)
product_ids = inserted_products.inserted_ids  # On récupère les IDs générés pour les lier aux commandes plus tard

# Étape 2 : Création de 20 clients
customers_list = []
for i in range(1, 21):  # Boucle pour générer 20 clients
    customer = {
        "firstName": f"Prénom{i}",
        "lastName": f"Nom{i}",
        "email": f"client{i}@exemple.com",  # Email fictif
        "city": random.choice(["Paris", "Lyon", "Marseille", "Bordeaux", "Lille"])
    }
    customers_list.append(customer)

# Insertion massive des 20 clients dans la collection 'customers'
inserted_customers = db.customers.insert_many(customers_list)
customer_ids = inserted_customers.inserted_ids  # On récupère les IDs des clients

# Étape 3 : Création de 100 commandes simulant des achats réels
orders_list = []
statuses = ["pending", "completed", "cancelled"]  # Différents états possibles d'une commande

for i in range(1, 101):  # On génère 100 commandes
    customer_id = random.choice(customer_ids)  # On choisit un client au hasard
    
    items_count = random.randint(1, 3)  # Chaque commande contient entre 1 et 3 types de produits
    order_items = []  # Liste des produits achetés dans cette commande
    total_amount = 0  # Montant total de la commande
    
    # On sélectionne des indices de produits au hasard sans doublons dans une même commande
    selected_indices = random.sample(range(len(product_ids)), items_count)
    
    for idx in selected_indices:
        prod_id = product_ids[idx]  # ID du produit
        prod_data = product_list[idx]  # Données du produit (pour le prix)
        qty = random.randint(1, 5)  # Quantité achetée (entre 1 et 5)
        price_at_purchase = prod_data["price"]  # On enregistre le prix AU MOMENT de l'achat (historisation)
        
        order_items.append({
            "productId": prod_id,  # Référence vers le produit
            "quantity": qty,
            "price": price_at_purchase  # On stocke le prix ici pour ne pas perdre la trace si le produit change de prix plus tard
        })
        total_amount += qty * price_at_purchase  # Cumul du montant
    
    # Date de création : un jour aléatoire sur les 30 derniers jours
    created_at = datetime.now() - timedelta(days=random.randint(0, 30))
    
    order = {
        "customerId": customer_id,  # Référence vers le client
        "items": order_items,       # Liste des produits
        "totalAmount": round(total_amount, 2), # Montant total arrondi
        "status": random.choice(statuses),     # État au hasard
        "createdAt": created_at                # Date
    }
    orders_list.append(order)

# Insertion massive des 100 commandes dans la collection 'orders'
db.orders.insert_many(orders_list)

print(f"--- Succès : 50 produits, 20 clients et 100 commandes insérés. ---")

# --- Tâche 3 : Requêtes analytiques ---

# Query (a) : Top 10 des produits ayant le plus gros stock
print("\n--- (a) Top 10 produits par stock décroissant ---")
# find() récupère tout, sort() trie (-1 pour décroissant), limit(10) prend les 10 premiers
top_stocks = db.products.find().sort("stock", -1).limit(10)
for p in top_stocks:
    print(f"Produit: {p['name']} | Stock: {p['stock']} | Catégorie: {p['category']}")

# Query (b) : Total des ventes (CA) par catégorie
print("\n--- (b) Total des ventes par catégorie de produits ---")
# On utilise un pipeline d'agrégation (une suite d'étapes de calcul)
pipeline_sales_by_cat = [
    {"$unwind": "$items"},  # 1. On sépare chaque item de la liste 'items' en un document distinct
    {
        "$lookup": {  # 2. On fait une jointure avec la collection 'products'
            "from": "products",
            "localField": "items.productId",
            "foreignField": "_id",
            "as": "product_info"
        }
    },
    {"$unwind": "$product_info"},  # 3. On "aplatit" le résultat du lookup qui était une liste
    {
        "$group": {  # 4. On regroupe par le nom de la catégorie
            "_id": "$product_info.category",
            # On somme le résultat de (quantité * prix)
            "totalSales": {"$sum": {"$multiply": ["$items.quantity", "$items.price"]}}
        }
    },
    {"$sort": {"totalSales": -1}}  # 5. On trie par CA décroissant
]

results_sales = db.orders.aggregate(pipeline_sales_by_cat)
for r in results_sales:
    print(f"Catégorie: {r['_id']} | Ventes Totales: {round(r['totalSales'], 2)}€")

# Query (c) : Clients "VIP" ayant dépensé plus de 1000€ au total
print("\n--- (c) Clients ayant dépensé plus de 1000 € ---")
pipeline_vip = [
    {
        "$group": {  # 1. On regroupe par client (ID)
            "_id": "$customerId",
            "totalSpent": {"$sum": "$totalAmount"} # On somme tous leurs achats
        }
    },
    {"$match": {"totalSpent": {"$gt": 1000}}}, # 2. On filtre ceux qui dépassent 1000
    {
        "$lookup": { # 3. On joint avec 'customers' pour avoir leurs noms/prénoms
            "from": "customers",
            "localField": "_id",
            "foreignField": "_id",
            "as": "user"
        }
    },
    {"$unwind": "$user"}, # 4. On aplatit l'info client
    {"$sort": {"totalSpent": -1}} # 5. On trie par dépense
]

vips = db.orders.aggregate(pipeline_vip)
for v in vips:
    name = f"{v['user']['firstName']} {v['user']['lastName']}"
    print(f"Client: {name} | Total Dépensé: {round(v['totalSpent'], 2)}€")

# --- Optimisation avec des Index (Tâche 4 suggérée) ---
# Les index permettent de ne pas scanner toute la base pour les recherches fréquentes
db.products.create_index([("stock", -1)]) # Pour le top stock
db.products.create_index([("category", 1)]) # Pour les filtres catégorie
db.orders.create_index([("customerId", 1)]) # Pour les jointures clients
db.orders.create_index([("status", 1)]) # Pour filtrer par statut de commande

print("\n--- Indexation terminée pour optimiser les performances. ---")
