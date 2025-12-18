"""
Cas d'usage : Création d'un ticket.

Ce module contient la logique applicative pour créer un nouveau ticket.
Il orchestre le domaine et les ports, sans dépendre d'aucune implémentation concrète.
"""

import uuid

# TODO: Décommenter une fois la classe Ticket implémentée (TD01)
# from src.domain.ticket import Ticket
from src.ports.ticket_repository import Ticket, TicketRepository


class CreateTicketUseCase:
    """
    Cas d'usage pour la création d'un ticket.

    Ce cas d'usage reçoit un repository via injection de dépendances.
    Il crée un nouveau ticket avec un identifiant unique et le persiste.

    Attributes:
        ticket_repo: Le repository pour sauvegarder le ticket
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le cas d'usage avec ses dépendances.

        Args:
            ticket_repo: L'implémentation du repository à utiliser
        """
        self.ticket_repo = ticket_repo

    def execute(self, title: str, description: str, creator_id: str) -> Ticket:
        """
        Exécute la création d'un ticket.

        Crée un nouveau ticket avec un UUID comme identifiant,
        le sauvegarde dans le repository et le retourne.

        Args:
            title: Titre du ticket
            description: Description détaillée du problème
            creator_id: Identifiant de l'utilisateur créant le ticket

        Returns:
            Le ticket créé avec son identifiant unique
        """
        ticket = Ticket(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            creator_id=creator_id,
        )
        self.ticket_repo.save(ticket)
        return ticket
