# Adapters - Implémentations Concrètes

> 🎯 **Rôle** : Connecter l'application au monde extérieur (HTTP, BDD, notifications...).

Ce dossier contient les **implémentations concrètes** des ports.

## Structure

```
adapters/
├── api/          # Adaptateur HTTP (FastAPI routes)
└── db/           # Adaptateurs de persistance (InMemory, SQLite...)
```

## Types d'adapters

### Adapters "Driving" (primaires)
Ceux qui **appellent** l'application :
- `api/` → Reçoit les requêtes HTTP et appelle les use cases

### Adapters "Driven" (secondaires)
Ceux que l'application **appelle** :
- `db/` → Implémente `TicketRepository` pour stocker les données

## Fichiers par TD

| Dossier | Fichier | Description | TD |
|---------|---------|-------------|-----|
| `db/` | `ticket_repository_inmemory.py` | Stockage en mémoire (tests) | Fourni |
| `db/` | `ticket_repository_sqlite.py` | Stockage SQLite | TD3 |
| `api/` | `ticket_router.py` | Routes REST `/tickets` | TD4 |

## Règles à respecter

✅ **Autorisé** :
- Imports de frameworks (`fastapi`, `sqlite3`...)
- Imports des ports (`from src.ports...`)
- Imports du domaine (`from src.domain...`)

❌ **Interdit** :
- Logique métier (doit rester dans `domain/`)
- Use cases (doivent rester dans `application/`)
