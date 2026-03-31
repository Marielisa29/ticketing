"""
Use case : Assigner un ticket à un agent.

Ce use case gère l'assignation d'un ticket existant à un agent.
"""

from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class AssignTicketUseCase:
    """
    Cas d'usage pour assigner un ticket à un agent.

    Orchestre la récupération du ticket, la vérification de son existence,
    l'application de la règle métier d'assignation (via l'entité), puis
    la persistance du ticket modifié.

    La règle métier (ex: interdiction d'assigner un ticket fermé) est portée
    par l'entité Ticket, pas par ce use case.
    """

    def __init__(self, ticket_repo: TicketRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            ticket_repo: Le repository de tickets (via son interface).
                         Peut être une implémentation InMemory, SQLite, PostgreSQL, etc.
        """
        self.ticket_repo = ticket_repo

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Assigne un ticket existant à un agent.

        Récupère le ticket par son identifiant, délègue l'assignation à
        l'entité Ticket (qui applique les règles métier), puis sauvegarde
        l'état mis à jour dans le repository.

        Args:
            ticket_id: Identifiant unique du ticket à assigner.
            agent_id: Identifiant de l'agent à qui assigner le ticket.

        Returns:
            Le ticket mis à jour avec son nouveau assignee_id.

        Raises:
            TicketNotFoundError: Si aucun ticket ne correspond à ticket_id.
            ValueError: Si le ticket est dans un état qui interdit l'assignation
                        (ex: ticket fermé — règle métier de l'entité Ticket).
        """
        ticket = self.ticket_repo.get_by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Ticket '{ticket_id}' introuvable.")

        ticket.assign(agent_id)

        self.ticket_repo.save(ticket)

        return ticket
