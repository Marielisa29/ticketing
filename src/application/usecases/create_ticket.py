"""
Use case : Créer un ticket.

Ce use case orchestre la création d'un ticket en utilisant les entités du domaine
et le port TicketRepository, sans dépendre d'une implémentation concrète.
"""

import uuid
from datetime import datetime, timezone

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class CreateTicketUseCase:
    """
    Cas d'usage pour créer un nouveau ticket.

    Orchestre la création d'un ticket en instanciant l'entité du domaine,
    en générant un identifiant unique (UUID) et en le persistant via le port.

    Reçoit le repository via injection de dépendances (principe d'inversion) :
    il ne connaît que l'interface TicketRepository, jamais l'implémentation concrète.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            ticket_repo: Le repository de tickets (via son interface).
                         Peut être une implémentation InMemory, SQLite, PostgreSQL, etc.
        """
        self.ticket_repo = ticket_repo

    def execute(
        self,
        title: str,
        description: str,
        creator_id: str,
    ) -> Ticket:
        """
        Exécute la création d'un ticket.

        Génère un UUID comme identifiant, horodate la création et la mise à jour
        au même instant (UTC), puis délègue la persistance au repository.

        Args:
            title: Titre du ticket. Ne peut pas être vide.
            description: Description détaillée du problème. Ne peut pas être vide.
            creator_id: Identifiant de l'utilisateur à l'origine du ticket.

        Returns:
            Le ticket créé et persisté, avec son identifiant généré,
            son statut initial OPEN et ses dates de création renseignées.

        Raises:
            ValueError: Si le titre ou la description sont vides
                        (règle métier levée par l'entité Ticket).
        """
        now = datetime.now(timezone.utc)

        ticket = Ticket(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            creator_id=creator_id,
            created_at=now,
            updated_at=now,
        )

        saved_ticket = self.ticket_repo.save(ticket)

        return saved_ticket
