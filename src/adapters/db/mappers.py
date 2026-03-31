"""
Mappers pour la conversion entre entités du domaine et lignes de base de données.

Ce module fournit des fonctions pour convertir les entités Ticket vers/depuis
les représentations de lignes SQLite.
"""

from datetime import datetime

from src.domain.priority import Priority
from src.domain.status import Status
from src.domain.ticket import Ticket
from src.domain.user import User


def ticket_to_row(ticket: Ticket) -> dict:
    """
    Convertit une entité Ticket du domaine en dictionnaire pour la base de données.

    Args:
        ticket: L'entité ticket à convertir

    Returns:
        Dictionnaire avec les noms de colonnes et valeurs prêts pour insertion SQL
    """
    return {
        "id": ticket.id,
        "title": ticket.title,
        "description": ticket.description,
        "creator_id": ticket.creator_id,
        "status": ticket.status.value,
        "priority": ticket.priority.value,
        "assignee_id": ticket.assignee_id,
        "project_id": ticket.project_id,
        "created_at": ticket.created_at.isoformat(),
        "updated_at": ticket.updated_at.isoformat(),
        "started_at": ticket.started_at.isoformat() if ticket.started_at else None,
        "closed_at": ticket.closed_at.isoformat() if ticket.closed_at else None,
    }


def row_to_ticket(row: dict) -> Ticket:
    """
    Convertit une ligne de base de données en entité Ticket du domaine.

    Args:
        row: Dictionnaire représentant une ligne de base de données (avec noms de colonnes comme clés)

    Returns:
        Entité Ticket du domaine
    """
    # Conversion des chaînes datetime
    created_at = datetime.fromisoformat(row["created_at"])
    updated_at = datetime.fromisoformat(row["updated_at"])
    started_at = (
        datetime.fromisoformat(row["started_at"]) if row["started_at"] else None
    )
    closed_at = datetime.fromisoformat(row["closed_at"]) if row["closed_at"] else None

    # Création du ticket sans status (il a une valeur par défaut)
    ticket = Ticket(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        creator_id=row["creator_id"],
        created_at=created_at,
        updated_at=updated_at,
        priority=Priority(row["priority"]),
        assignee_id=row["assignee_id"],
        project_id=row["project_id"],
        started_at=started_at,
        closed_at=closed_at,
    )

    # Restauration du status réel depuis la base de données avec la méthode dédiée
    ticket._restore_status_from_db(Status(row["status"]))

    return ticket


def user_to_row(user: User) -> dict:
    """
    Convertit une entité User en dictionnaire pour SQLite.

    Args:
        user: L'utilisateur à convertir

    Returns:
        Dictionnaire avec les colonnes SQL
    """
    return {
        "id": user.id,
        "username": user.username,
        "is_agent": 1 if user.is_agent else 0,
        "is_admin": 1 if user.is_admin else 0,
    }


def row_to_user(row: dict) -> User:
    """
    Convertit une ligne SQL en entité User.

    Args:
        row: Dictionnaire représentant une ligne de la table users

    Returns:
        L'entité User reconstituée
    """
    return User(
        id=row["id"],
        username=row["username"],
        is_agent=bool(row["is_agent"]),
        is_admin=bool(row["is_admin"]),
    )
