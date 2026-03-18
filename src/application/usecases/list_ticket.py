"""
Use case : Lister les tickets.

Ce use case récupère tous les tickets du système,
avec un filtre optionnel par statut.
"""

from typing import Optional

from src.domain.ticket import Ticket
from src.domain.status import Status
from src.ports.ticket_repository import TicketRepository


class ListTicketsUseCase:
    """
    Cas d'usage pour lister les tickets.

    Permet de récupérer tous les tickets, ou uniquement ceux
    correspondant à un statut donné.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case.

        Args:
            ticket_repo: Le repository de tickets
        """
        self.ticket_repo = ticket_repo

    def execute(self, status: Optional[Status] = None) -> list[Ticket]:
        """
        Retourne la liste des tickets, filtrée par statut si fourni.

        Args:
            status: Statut pour filtrer les tickets (optionnel).
                    Si None, retourne tous les tickets.

        Returns:
            Liste des tickets correspondant au filtre
        """
        tickets = self.ticket_repo.list_all()

        if status is not None:
            tickets = [t for t in tickets if t.status == status]

        return tickets
