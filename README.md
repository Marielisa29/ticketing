# Ticketing Starter 🎫 Module R4.01 Architecture logicielle (BUT2)

Année 2025/2026 - Enseignant : Marc Ennaji (marc.ennaji@univ-rennes.fr)

> **Template de démarrage** pour le projet pédagogique R4.01 — Architecture hexagonale

Ce dépôt est un **squelette d'application** prêt à l'emploi, pour le projet de gestion de tickets. Il fournit :
- ✅ L'arborescence des principaux répertoires du projet (domain, ports, adapters, application)
- ✅ La configuration automatique des outils (pre-commit, pytest, ruff)
- ✅ Des fichiers TODO à compléter progressivement
- ✅ Des tests exemples à décommenter

**Objectif** : Vous permettre de vous concentrer sur l'apprentissage de l'architecture hexagonale, sans perdre de temps sur la configuration initiale.

---

## 📚 Documentation complète

**Tous les guides et TDs sont dans le repository de ressources :**

👉 https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources

### Liens directs essentiels

- [📖 Guide de démarrage](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/demarrage.md) ⚠️ **À suivre AVANT le TD0**
- [🔄 Workflow Git/GitHub](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/workflow_de_developpement.md)
- [🧪 Guide des tests](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/comment_tester.md)

---

## 🚀 Démarrage rapide

**Première utilisation ?** Suivez le [Guide de démarrage](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/demarrage.md) pas à pas.

**Commandes essentielles** (après installation) :
```bash
# Initialiser l'environnement (à faire avant chaque TD)
source scripts/init.sh

# Lancer le serveur
uvicorn src.main:app --reload   # → http://localhost:8000

# Lancer les tests
pytest
```

---

## 📁 Structure du projet

```
ticketing_starter/
├── docs/               # Documentation spécifique au projet
├── scripts/            # Scripts utilitaires (init.sh)
├── tests/              # Tests par couche (domain, application, e2e)
├── src/
│   ├── domain/         # Logique métier pure (aucune dépendance externe)
│   ├── ports/          # Interfaces abstraites (ABC)
│   ├── application/    # Cas d'utilisation (use cases)
│   ├── adapters/       # Implémentations concrètes (API, BDD)
│   └── main.py         # Racine de composition (câblage des dépendances)
├── requirements.txt    # Dépendances Python
├── pyproject.toml      # Configuration projet (ruff, pytest)
└── .pre-commit-config.yaml  # Hooks de formatage automatique
```

Chaque dossier contient un `README.md` rappelant son rôle et ses règles.

Pour comprendre l'architecture en détail, consultez le [CM sur l'architecture hexagonale](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/cm/CM1_Fondamentaux_architecture.md#-4-architecture-hexagonale-ports--adapters).

### 📐 Arborescence obligatoire

⚠️ **IMPORTANT** : L'arborescence de base (`src/domain/`, `src/ports/`, `src/application/`, `src/adapters/`, `tests/`) est **obligatoire et identique pour tous les étudiants**.

**✅ Autorisé** : Créer des sous-dossiers à l'intérieur (ex: `src/domain/entities/`, `src/adapters/db/repositories/`)

**❌ Interdit** : Renommer, déplacer ou supprimer les dossiers principaux

Cette contrainte permet à tous de travailler sur une base commune et facilite l'accompagnement pédagogique.

---

## 🎯 Objectifs pédagogiques

- Comprendre la séparation Domain / Application / Adapters
- Implémenter des ports (interfaces) et leurs adapters
- Appliquer l'**inversion de dépendances** et le câblage dans `main.py`
- Écrire des tests par couche (unitaires, intégration, end-to-end)

---

## 📋 Bonnes pratiques attendues

| Pratique | Description |
|----------|-------------|
| **Commits fréquents** | Un commit = une unité de travail logique (fonction, fix, refactoring) |
| **Refactoring continu** | Améliorez le code au fur et à mesure (renommages, extractions, nettoyage) |
| **Messages de commits clairs** | Décrivez ce qui a été fait, pas comment |

Voir le [Guide de workflow](https://github.com/Marcennaji/architecture-logicielle-BUT2-ressources/blob/main/td/guides/workflow_de_developpement.md) pour le processus complet de rendu via tags Git.
