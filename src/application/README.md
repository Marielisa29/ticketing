# Application - Cas d'Usage

> 🎯 **Rôle** : Orchestrer le domaine et les ports pour réaliser une action métier.

Ce dossier contient les **use cases** (cas d'utilisation) de l'application.

## Structure

```
application/
└── usecases/
    ├── create_ticket.py    # Créer un nouveau ticket
    └── ...                  # Autres use cases à implémenter
```

## Fichiers à implémenter

| Use Case | Description | TD |
|----------|-------------|-----|
| `CreateTicketUseCase` | Crée un ticket et le persiste | TD2 |
| `ListTicketsUseCase` | Récupère tous les tickets | TD2 |
| `AssignTicketUseCase` | Assigne un ticket à un agent | TD2 |
| `CloseTicketUseCase` | Ferme un ticket | TD2 |

## Pattern d'un Use Case

```python
class MonUseCase:
    def __init__(self, repository: TicketRepository):
        """Injection des dépendances via le constructeur."""
        self.repository = repository

    def execute(self, ...params) -> ResultType:
        """Point d'entrée unique du use case."""
        # 1. Valider les entrées
        # 2. Appeler le domaine
        # 3. Utiliser les ports (repository...)
        # 4. Retourner le résultat
```

## Règles à respecter

✅ **Autorisé** :
- Imports du domaine (`from src.domain...`)
- Imports des ports (`from src.ports...`)

❌ **Interdit** :
- Imports d'adapters concrets (pas de `InMemoryRepository` ici)
- Logique HTTP (pas de `Request`, `Response`)

Les adapters sont injectés au runtime dans `main.py`.
