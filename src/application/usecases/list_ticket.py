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

    Récupère l'ensemble des tickets persistés et applique un filtre
    optionnel par statut. Le filtrage est effectué en mémoire après
    récupération, ce qui convient à l'adaptateur InMemory et aux petits
    volumes. Un adaptateur SQL pourrait optimiser cela avec une clause WHERE.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            ticket_repo: Le repository de tickets (via son interface).
                         Peut être une implémentation InMemory, SQLite, PostgreSQL, etc.
        """
        self.ticket_repo = ticket_repo

    def execute(self, status: Optional[Status] = None) -> list[Ticket]:
        """
        Retourne la liste des tickets, filtrée par statut si fourni.

        Ne modifie pas l'état du repository ni des tickets retournés.
        Si aucun ticket ne correspond au filtre, retourne une liste vide.

        Args:
            status: Statut pour filtrer les tickets (optionnel).
                    Valeurs possibles : Status.OPEN, Status.IN_PROGRESS,
                    Status.RESOLVED, Status.CLOSED.
                    Si None, tous les tickets sont retournés sans filtre.

        Returns:
            Liste des tickets correspondant au filtre, dans l'ordre
            d'insertion dans le repository. Peut être vide.
        """
        tickets = self.ticket_repo.list_all()

        if status is not None:
            tickets = [t for t in tickets if t.status == status]

        return tickets
