# Module 1 : Introduction aux Bases de Données NoSQL

## 1. Pourquoi le NoSQL ? (Not Only SQL)

### Le Problème des Bases Relationnelles (SQL)
Historiquement, les bases de données relationnelles (comme MySQL, PostgreSQL, Oracle) dominaient le marché. Elles sont excellentes pour :
- La cohérence stricte des données (Transactions ACID).
- Les relations complexes entre tables (Jointures).
- La structure rigide (Schéma défini à l'avance).

**Mais** avec l'arrivée du Big Data et du Web moderne, elles ont montré leurs limites :
1. **Scalabilité Verticale (Coûteuse)** : Pour gérer plus de données, il faut un serveur plus puissant (plus de RAM, plus de CPU). C'est cher et limité physiquement.
2. **Rigidité du Schéma** : Modifier la structure d'une table avec des milliards de lignes est très lent et complexe.
3. **Données Non-Structurées** : Difficile de stocker efficacement des documents JSON, des graphes sociaux ou des logs en temps réel.

### La Réponse NoSQL
Le NoSQL est né pour répondre à ces défis. Ce n'est pas "Non au SQL", mais "Pas Seulement du SQL".

**Les avantages clés :**
- **Scalabilité Horizontale** : On ajoute simplement des petits serveurs (nœuds) pour augmenter la capacité ("Scale Out").
- **Schéma Flexible (Schemaless)** : On peut stocker des données hétérogènes sans définir de structure fixe avant.
- **Performance** : Optimisé pour des cas d'usages spécifiques (lecture rapide, écriture massive, etc.).

---

## 2. Le Théorème CAP (Brewer)

C'est LE concept fondamental pour comprendre les systèmes distribués. Il stipule qu'un système de stockage distribué ne peut garantir simultanément que **deux** des trois propriétés suivantes :

1. **C (Consistency - Cohérence)** :
   - Chaque lecture reçoit l'écriture la plus récente ou une erreur.
   - *Tous les nœuds voient la même donnée au même moment.*
   
2. **A (Availability - Disponibilité)** :
   - Chaque requête reçoit une réponse (sans garantie que ce soit la plus récente).
   - *Le système reste opérationnel même si des nœuds plantent.*
   
3. **P (Partition Tolerance - Tolérance au Partitionnement)** :
   - Le système continue de fonctionner malgré des coupures réseau entre les nœuds.
   - *Dans un système distribué (Big Data), le partitionnement réseau est inévitable. Donc le "P" est souvent obligatoire.*

### Le Choix Cornélien : CP ou AP ?
Puisque "P" est quasi-obligatoire dans le Cloud/Big Data, on doit choisir entre :

- **CP (Consistency + Partition Tolerance)** :
  - Priorité à la cohérence. Si le réseau coupe, on bloque les écritures pour éviter les données divergentes.
  - *Exemple : MongoDB (par défaut), HBase, Redis (Configuration cluster spécifique).*
  - *Usage : Banques, Stocks, Gestion d'inventaire critique.*

- **AP (Availability + Partition Tolerance)** :
  - Priorité à la disponibilité. Si le réseau coupe, on continue de répondre, même avec des données potentiellement anciennes ("Eventual Consistency").
  - *Exemple : Cassandra, DynamoDB, CouchDB.*
  - *Usage : Réseaux sociaux (Likes, Flux), Logs, IoT, Recommandations.*

*(Note : Les bases SQL traditionnelles sont souvent CA, car elles tournent généralement sur un seul serveur, donc pas de partitionnement réseau à gérer).*

---

## 3. Les 4 Grandes Familles de NoSQL

Il n'y a pas un seul type de NoSQL, mais quatre familles principales, chacune adaptée à un besoin précis.

### Type 1 : Document (Ex: **MongoDB**)
- **Données :** Stockées sous forme de documents (souvent JSON ou BSON).
- **Structure :** Hiérarchique, flexible (champs peuvent varier d'un document à l'autre).
- **Cas d'usage :**
  - Catalogues de produits (E-commerce).
  - Gestion de contenu (CMS).
  - Profils utilisateurs.
  - Applications Web/Mobile agiles.
- **Forces :** Modélisation intuitive pour les développeurs (Objet -> JSON), requêtes complexes possibles.

### Type 2 : Colonnes (Ex: **Cassandra**, HBase)
- **Données :** Stockées par colonnes plutôt que par lignes. Une ligne peut avoir des millions de colonnes.
- **Structure :** Familles de colonnes. Très optimisé pour l'écriture.
- **Cas d'usage :**
  - Séries temporelles (IoT, capteurs, météo).
  - Logs d'activité (Audit, Tracking).
  - Messageries (Facebook Messenger, Discord).
- **Forces :** Performance d'écriture phénoménale, scalabilité linéaire massive.

### Type 3 : Clé-Valeur (Ex: **Redis**, DynamoDB)
- **Données :** Un dictionnaire géant. Une clé unique pointe vers une valeur (chaîne, liste, set...).
- **Structure :** Très simple. Pas de requêtes complexes (pas de "WHERE age > 18").
- **Cas d'usage :**
  - Caching (Mise en cache de résultats de requêtes lentes).
  - Gestion de sessions utilisateur (Panier d'achat).
  - Files d'attente (Queues).
  - Classements temps réel (Leaderboards jeux vidéo).
- **Forces :** Vitesse extrême (souvent en mémoire RAM), simplicité.

### Type 4 : Graphe (Ex: **Neo4j**, Amazon Neptune)
- **Données :** Nœuds (entités) et Arcs (relations).
- **Structure :** Le réseau est la structure.
- **Cas d'usage :**
  - Réseaux sociaux (Amis d'amis).
  - Moteurs de recommandation ("Les gens qui ont acheté X ont aussi acheté Y").
  - Détection de fraude (Réseaux de blanchiment).
  - Itinéraires (GPS).
- **Forces :** Traverser des relations complexes très rapidement (ce qui tuerait une base SQL avec trop de JOINs).

---

## Conclusion
Un bon Data Engineer ne cherche pas "la meilleure base de données", mais **la base adaptée au problème**.
- Besoin de flexibilité et prototypage rapide ? -> **MongoDB**
- Besoin d'écrire des millions de logs/sec et ne jamais perdre une donnée ? -> **Cassandra**
- Besoin de réponses en millisecondes pour un site à fort trafic ? -> **Redis**
