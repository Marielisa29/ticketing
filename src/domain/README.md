# Domain - Couche Métier

> 🎯 **Règle d'or** : Aucune dépendance externe ici !

Ce dossier contient la **logique métier pure** du système de ticketing.

## Fichiers

| Fichier | Description | TD |
|---------|-------------|-----|
| `status.py` | Énumération des statuts de ticket | TD1 |
| `user.py` | Entité User (utilisateur du système) | TD1 |
| `ticket.py` | Entité Ticket (cœur du domaine) | TD1 |
| `exceptions.py` | Erreurs métier personnalisées | Fourni |

## Règles à respecter

✅ **Autorisé** :
- Imports de la bibliothèque standard Python (`dataclasses`, `enum`, `datetime`...)
- Imports internes au dossier `domain/`

❌ **Interdit** :
- `import fastapi` → c'est de l'infrastructure
- `import sqlalchemy` → c'est de la persistance
- `from src.adapters...` → dépendance vers l'extérieur
- `from src.ports...` → le domaine ne connaît pas les ports

## Pourquoi ces restrictions ?

Le domaine doit être **testable en isolation** et **réutilisable** :
- Pas besoin de serveur web pour tester un `Ticket`
- Pas besoin de base de données pour valider les règles métier
- Si on change de framework (FastAPI → Flask), le domaine reste intact
