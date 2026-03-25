## Adaptateurs de persistance

### TicketRepository

**Implémentations disponibles** :
- `InMemoryTicketRepository` : Stockage en mémoire (tests)
- `SQLiteTicketRepository` : Stockage SQLite (production)

**Interchangeabilité** : Les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implémentation se fait à l'instanciation (injection de dépendances).


Q6 — On peut passer facilement d’InMemory à SQLite parce que les deux implémentations respectent le même contrat : l’interface TicketRepository expose les mêmes méthodes (save, get_by_id, list_all) et les use cases dépendent de cette interface, pas d’une implémentation concrète. Grâce à l’injection de dépendances, il suffit donc de fournir une instance différente du repository au moment de construire le use case ou dans les fixtures de test ; la logique métier et les tests restent identiques (ou demandent uniquement un ajustement du setup), car la transformation des entités vers le stockage est confiée aux adaptateurs et mappers.

Q7 — Si on passe à PostgreSQL, le noyau de l’application (les use cases et le domaine) ne change pas. Les fichiers qui changeraient sont les adaptateurs et la configuration d’infrastructure : on ajoutera un nouveau repository concret, par exemple src/adapters/db/ticket_repository_postgres.py, éventuellement un module de connexion/configuration (par ex. src/adapters/db/postgres_connection.py) et les scripts/migrations SQL (ou fichiers Alembic). Les tests d’intégration et les fixtures (tests/conftest.py) devront être adaptés pour fournir une instance PostgreSQL (ou utiliser testcontainers), et les mappers peuvent nécessiter de petits ajustements si les types/formatages diffèrent. Tout le reste (src/application/* et src/domain/*) reste inchangé.

Q8 — Avoir à la fois InMemory et SQLite apporte une complémentarité utile pour la qualité et la vitesse des tests ainsi que pour la robustesse du code. InMemory permet des tests unitaires très rapides, simples et déterministes sans I/O, ce qui accélère le développement. SQLite fournit des tests d’intégration plus réalistes qui valident la sérialisation, le schéma SQL et les comportements liés à la base (types, contraintes, requêtes). En combinant les deux, on réduit les faux positifs/negatifs : InMemory vérifie la logique métier pure tandis que SQLite attrape les problèmes liés à la persistance réelle, ce qui facilite la migration ultérieure vers d’autres bases (Postgres, MySQL) et augmente la confiance globale dans le système.