## Adaptateurs de persistance

### TicketRepository

**Implémentations disponibles** :
- `InMemoryTicketRepository` : Stockage en mémoire (tests)
- `SQLiteTicketRepository` : Stockage SQLite (production)

**Interchangeabilité** : Les use cases utilisent uniquement le port `TicketRepository`.
Le choix de l'implémentation se fait à l'instanciation (injection de dépendances).
