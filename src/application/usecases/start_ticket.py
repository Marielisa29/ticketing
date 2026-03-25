"""
Use case : Démarrer un ticket.

Ce use case gère le démarrage du traitement d'un ticket existant.
"""

from src.domain.exceptions import TicketNotFoundError
from src.domain.ticket import Ticket
from src.ports.clock import Clock
from src.ports.ticket_repository import TicketRepository


class StartTicketUseCase:
    """
    Cas d'usage pour démarrer le traitement d'un ticket.

    Dépendances injectées :
    - Horloge (Clock) : pour obtenir la date/heure de démarrage
    - Repository : pour récupérer et sauvegarder le ticket
    """

    def __init__(self, ticket_repo: TicketRepository, clock: Clock):
        """
        Initialise le use case avec ses dépendances.

        Args:
            ticket_repo: Le repository de tickets
            clock: L'horloge pour obtenir l'heure actuelle
        """
        self.ticket_repo = ticket_repo
        self.clock = clock

    def execute(self, ticket_id: str, agent_id: str) -> Ticket:
        """
        Démarre le traitement d'un ticket.

        Étapes:
        1. Récupérer le ticket depuis le repository
        2. Vérifier son existence
        3. Obtenir la date/heure actuelle depuis l'horloge
        4. Appeler la méthode start() du ticket (qui valide les règles métier)
        5. Sauvegarder le ticket modifié
        6. Retourner le ticket

        Args:
            ticket_id: ID du ticket à démarrer
            agent_id: ID de l'agent qui démarre le ticket

        Returns:
            Le ticket mis à jour avec started_at renseigné

        Raises:
            TicketNotFoundError: Si le ticket n'existe pas
            TicketNotAssignedError: Si le ticket n'est pas assigné
            WrongAgentError: Si agent_id != assignee_id
            InvalidTicketStateError: Si le statut n'est pas OPEN
        """
        # Récupérer le ticket
        ticket = self.ticket_repo.get_by_id(ticket_id)

        # Vérifier son existence
        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        # Obtenir l'heure actuelle
        started_at = self.clock.now()

        # Démarrer le ticket (avec validations métier)
        ticket.start(agent_id, started_at)

        # Sauvegarder
        self.ticket_repo.save(ticket)

        # Retourner
        return ticket
