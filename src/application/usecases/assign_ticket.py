"""
Use case : Assigner un ticket à un agent.

Ce use case gère l'assignation d'un ticket existant à un agent.
"""

from src.domain.ticket import Ticket
from src.domain.exceptions import TicketNotFoundError
from src.ports.ticket_repository import TicketRepository


class AssignTicketUseCase:
    """
    Cas d'usage pour assigner un ticket à un agent.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case.

        Args:
            ticket_repo: Le repository de tickets
        """
        self.ticket_repo = ticket_repo

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Assigne un ticket à un agent.

        Args:
            ticket_id: ID du ticket à assigner
            agent_id: ID de l'agent assigné

        Returns:
            Le ticket mis à jour

        Raises:
            TicketNotFoundError: Si le ticket n'existe pas
            ValueError: Si le ticket est fermé (règle métier du domaine)
        """
        ticket = self.ticket_repo.get_by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' introuvable.")

        ticket.assign(agent_id)

        self.ticket_repo.save(ticket)

        return ticket
