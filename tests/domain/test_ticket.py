"""
Tests unitaires pour le domaine (TD1).

Ces tests vérifient le comportement des entités du domaine.
Ils doivent passer sans aucune dépendance externe (pas de DB, pas d'API).

Écrivez vos tests ici après avoir implémenté les classes dans src/domain/.
Lancez-les avec : pytest tests/domain/
"""

import pytest

from src.domain.status import Status
from src.domain.ticket import Ticket
from src.domain.user import User


def test_status_values_exist():
    """Vérifie que les 4 statuts existent."""
    assert Status.OPEN.value == "open"
    assert Status.IN_PROGRESS.value == "in_progress"
    assert Status.RESOLVED.value == "resolved"
    assert Status.CLOSED.value == "closed"


def test_user_creation():
    """Vérifie la création d'un utilisateur."""
    user = User(id="u1", username="alice")
    assert user.id == "u1"
    assert user.username == "alice"
    assert not user.is_agent
    assert not user.is_admin


def test_ticket_creation():
    """Vérifie la création d'un ticket avec valeurs par défaut."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )
    assert ticket.status == Status.OPEN
    assert ticket.assignee_id is None


def test_ticket_assign():
    """Vérifie l'assignation d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.assign("agent1")
    assert ticket.assignee_id == "agent1"


def test_ticket_close():
    """Vérifie la fermeture d'un ticket."""
    ticket = Ticket(id="t1", title="Test", description="desc", creator_id="u1")
    ticket.close()
    assert ticket.status == Status.CLOSED


# Tests règles métiers


def test_cannot_assign_closed_ticket():
    """Règle : Un ticket fermé ne peut plus être assigné."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
        status=Status.CLOSED,
    )

    with pytest.raises(ValueError, match="Cannot assign a closed ticket"):
        ticket.assign("user2")  # Tentative d'assignation


def test_cannot_close_already_closed_ticket():
    """Règle : Un ticket déjà fermé ne peut pas être re-fermé."""
    ticket = Ticket(
        id="t1",
        title="Bug connexion",
        description="Impossible de se connecter",
        creator_id="user1",
    )

    # Fermer le ticket une première fois
    ticket.close()

    # Tenter de fermer le ticket à nouveau
    with pytest.raises(ValueError, match="Ticket is already closed"):
        ticket.close()  # Cela devrait lever une exception


def test_ticket_title_cannot_be_empty():
    """Règle : Un ticket doit avoir un titre non vide."""

    with pytest.raises(ValueError, match="Ticket title cannot be empty."):
        Ticket(
            id="t1",
            title="",  # Titre vide
            description="Une description",
            creator_id="user1",
        )


# def test_user_username_cannot_be_empty():
#     """Règle : Un utilisateur doit avoir un username non vide."""

#     with pytest.raises(ValueError, match="Ticket title cannot be empty."):
#         User(
#             id="u1",
#             username="",  # Username vide
#             is_agent=False,
#             is_admin=False
#         )


# def test_user_roles():
#     """Règle : Un utilisateur peut avoir un rôle."""

#     user = User(
#         id="u1",
#         username="alice",
#         is_agent=True,
#         is_admin=False
#     )

#     assert user.is_agent is True
#     assert user.is_admin is False

#     user2 = User(
#         id="u2",
#         username="bob",
#         is_agent=False,
#         is_admin=True
#     )

#     assert user2.is_agent is False
#     assert user2.is_admin is True
