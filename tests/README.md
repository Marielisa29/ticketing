# Tests

> 🎯 **Objectif** : Tester chaque couche de manière isolée.

## Structure

```
tests/
├── domain/        # Tests unitaires du domaine (TD1)
├── application/   # Tests des use cases (TD2)
└── e2e/           # Tests end-to-end de l'API (TD4)
```

## Organisation par couche

| Dossier | Ce qu'on teste | Comment | Dépendances |
|---------|---------------|---------|-------------|
| `domain/` | Entités, règles métier | Instanciation directe | Aucune |
| `application/` | Use cases | Injection de fakes (InMemory) | Domaine |
| `e2e/` | API complète | `TestClient` HTTP | Tout |

## Commandes

```bash
# Tous les tests
pytest

# Tests d'une couche spécifique
pytest tests/domain/
pytest tests/application/
pytest tests/e2e/

# Avec couverture
pytest --cov=src

# Mode verbose
pytest -v
```

## État actuel

Les tests sont **désactivés par défaut** via `pytest.skip()`.  
Décommentez-les au fur et à mesure de votre avancement :

1. **TD1** → Activez `tests/domain/test_ticket.py`
2. **TD2** → Activez `tests/application/test_create_ticket.py`
3. **TD4** → Activez les tests dans `tests/e2e/test_api.py`

## Stratégie de test

Voir le [Guide des tests](../docs/tests.md) pour choisir entre :
- **Approche traditionnelle** : Code d'abord, tests ensuite
- **TDD** : Tests d'abord, code ensuite
