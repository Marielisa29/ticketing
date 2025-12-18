## 📌 Contexte

**TD concerné :** TD0 / TD1 / TD2 / TD3 / TD4 *(supprimer les non concernés)*  
**Branche :** `tdX` → `main`

**Résumé du travail réalisé :**
<!-- Décrivez brièvement ce que vous avez implémenté (facultatif) -->

---

## ✅ Checklist architecture hexagonale

**Obligatoire - Principes fondamentaux :**

- [ ] Le **domaine** ne dépend d'aucune librairie technique (FastAPI, SQLite, etc.)
- [ ] Aucune couche **infrastructure/adapters** n'est importée par le domaine
- [ ] Les dépendances pointent **vers l'intérieur** (adapters → application → domain)
- [ ] Les **responsabilités** sont clairement séparées (domain / application / adapters)
- [ ] Les **ports** (interfaces) sont définis dans le domaine, implémentés dans les adapters

---

## ✅ Checklist tests

- [ ] Les **règles métier** sont testées **sans** infrastructure (tests unitaires du domain)
- [ ] Les tests **ne dépendent pas** d'un serveur web ou d'une vraie base de données
- [ ] **Tous les tests passent** localement (`pytest` en vert ✅)
- [ ] Les tests sont **lisibles** et vérifient un comportement précis, reflétés par un nom explicite

---

## ✅ Checklist qualité du code

- [ ] Le code est **formaté** (pre-commit hook passé sans erreur)
- [ ] Pas de code commenté inutile
- [ ] Les noms de variables/fonctions sont **explicites**
- [ ] Les commits ont des messages **clairs** et en français

---

## 🧩 Checklist spécifique au TD

<!-- Cochez les éléments demandés dans l'énoncé du TD -->

**Exemple TD1 (Modélisation du domaine) :**
- [ ] Les entités `Ticket` et `User` sont créées
- [ ] L'enum `Status` contient les 4 états requis
- [ ] Les règles métier sont dans les méthodes de `Ticket`
- [ ] Les tests du domaine passent

---

## 📝 Questions / remarques pour l'enseignant

<!-- 
Utilisez cette section pour :
- Poser des questions sur des choix d'implémentation
- Signaler des doutes ou points à clarifier
- Expliquer des choix techniques si nécessaire
-->



---

## 🔍 Aide-mémoire pour la review

**Pour l'enseignant :** Points d'attention prioritaires selon le TD
- **TD1** : Respect de l'architecture hexagonale (zéro import technique dans domain)
- **TD2** : Injection de dépendances correcte dans les use cases
- **TD3** : Repository implémente bien l'interface définie dans ports
- **TD4** : L'API ne contient pas de logique métier
