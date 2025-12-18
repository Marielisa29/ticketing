# Ports - Interfaces Abstraites

> 🎯 **Définition** : Un port est un **contrat** (interface) que les adapters doivent respecter.

Ce dossier contient les **interfaces abstraites** (ABC) qui définissent comment le domaine communique avec l'extérieur.

## Fichiers

| Fichier | Description | TD |
|---------|-------------|-----|
| `ticket_repository.py` | Interface pour la persistance des tickets | TD2 |

## Concept clé : Inversion de dépendances

```
Sans inversion :  UseCase → SQLiteRepository (dépendance directe)
Avec inversion :  UseCase → TicketRepository (interface) ← SQLiteRepository
```

Le **domaine définit le contrat**, les adapters l'implémentent.

## Comment créer un port ?

```python
from abc import ABC, abstractmethod

class MonPort(ABC):
    @abstractmethod
    def ma_methode(self, param: str) -> bool:
        """Description de ce que fait la méthode."""
        raise NotImplementedError
```

## Règles à respecter

✅ **Autorisé** :
- Imports du domaine (`from src.domain.ticket import Ticket`)
- Bibliothèque standard (`abc`, `typing`)

❌ **Interdit** :
- Imports d'adapters (pas de `import sqlite3` ici)
- Implémentation concrète (uniquement des méthodes abstraites)
