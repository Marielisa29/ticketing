"""
Tests unitaires pour le domaine (TD1).

Ces tests vérifient le comportement des entités du domaine.
Ils doivent passer sans aucune dépendance externe (pas de DB, pas d'API).

Écrivez vos tests ici après avoir implémenté les classes dans src/domain/.
Lancez-les avec : pytest tests/domain/
"""

# TODO (TD1): Décommenter ces imports une fois les classes implémentées
# import pytest
# from src.domain.status import Status
# from src.domain.ticket import Ticket
# from src.domain.user import User


# ==========================================================================
# EXEMPLES DE TESTS À ÉCRIRE (décommentez et adaptez)
# ==========================================================================

# def test_status_values_exist():
#     """Vérifie que les 4 statuts existent."""
#     assert Status.OPEN.value == "open"
#     assert Status.IN_PROGRESS.value == "in_progress"
#     assert Status.RESOLVED.value == "resolved"
#     assert Status.CLOSED.value == "closed"


# def test_user_creation():
#     """Vérifie la création d'un utilisateur."""
#     user = User(id="u1", username="alice")
#     assert user.id == "u1"
#     assert user.username == "alice"


# def test_ticket_creation():
#     """Vérifie la création d'un ticket avec valeurs par défaut."""
#     ticket = Ticket(
#         id="t1",
#         title="Bug connexion",
#         description="Impossible de se connecter",
#         creator_id="user1",
#     )
#     assert ticket.status == Status.OPEN
#     assert ticket.assignee_id is None


# def test_ticket_assign():
#     """Vérifie l'assignation d'un ticket."""
#     ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
#     ticket.assign("agent1")
#     assert ticket.assignee_id == "agent1"


# def test_ticket_close():
#     """Vérifie la fermeture d'un ticket."""
#     ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
#     ticket.close()
#     assert ticket.status == Status.CLOSED


# ==========================================================================
# TESTS DES RÈGLES MÉTIER (invariants) - à vous de les écrire !
# ==========================================================================

# def test_cannot_assign_closed_ticket():
#     """Règle : Un ticket fermé ne peut plus être assigné."""
#     # TODO: Implémenter ce test
#     pass


# def test_cannot_close_already_closed_ticket():
#     """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
#     # TODO: Implémenter ce test
#     pass


# def test_ticket_title_cannot_be_empty():
#     """Règle : Un ticket doit avoir un titre non vide."""
#     # TODO: Implémenter ce test
#     pass
