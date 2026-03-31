"""
Tests du use case StartTicket.

Ces tests vérifient que le use case orchestre correctement
le domaine (validation métier), le port Clock et le repository.
"""

from datetime import datetime, timezone

import pytest

from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.adapters.fixed_clock import FixedClock
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.start_ticket import StartTicketUseCase
from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    TicketNotFoundError,
    WrongAgentError,
)
from src.domain.status import Status


class TestStartTicketUseCase:
    """Suite de tests pour le démarrage de tickets."""

    def setup_method(self):
        """Initialise le repository, l'horloge et les use cases."""
        self.repo = InMemoryTicketRepository()

        # Horloge fixe pour les tests (déterministe)
        self.fixed_time = datetime(2026, 1, 16, 14, 30, 0, tzinfo=timezone.utc)
        self.clock = FixedClock(self.fixed_time)

        # Use cases
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)
        self.start_use_case = StartTicketUseCase(self.repo, self.clock)

    def test_start_ticket_success(self):
        """Doit démarrer un ticket assigné avec succès."""
        # Arrange - Créer et assigner un ticket
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)

        # Act - Démarrer le ticket
        started_ticket = self.start_use_case.execute(ticket.id, agent_id)

        # Assert
        assert started_ticket.status == Status.IN_PROGRESS
        assert started_ticket.started_at == self.fixed_time
        assert started_ticket.assignee_id == agent_id

    def test_start_ticket_not_found(self):
        """Doit lever TicketNotFoundError si le ticket n'existe pas."""
        # Act & Assert
        with pytest.raises(TicketNotFoundError):
            self.start_use_case.execute("ticket-inexistant", "agent-789")

    def test_start_ticket_invalid_status(self):
        """Doit lever InvalidTicketStateError si le ticket n'est pas OPEN."""
        # Arrange - Créer, assigner et démarrer un ticket
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)
        self.start_use_case.execute(ticket.id, agent_id)

        # Act & Assert - Essayer de le redémarrer (il est déjà IN_PROGRESS)
        with pytest.raises(InvalidTicketStateError):
            self.start_use_case.execute(ticket.id, agent_id)

    def test_start_ticket_not_assigned(self):
        """Doit lever TicketNotAssignedError si le ticket n'est pas assigné."""
        # Arrange - Créer un ticket sans l'assigner
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )

        # Act & Assert
        with pytest.raises(TicketNotAssignedError):
            self.start_use_case.execute(ticket.id, "agent-789")

    def test_start_ticket_wrong_agent(self):
        """Doit lever WrongAgentError si l'agent ne correspond pas."""
        # Arrange - Créer et assigner un ticket à agent-456
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        assigned_agent = "agent-456"
        self.assign_use_case.execute(ticket.id, assigned_agent)

        # Act & Assert - Essayer avec un autre agent
        wrong_agent = "agent-999"
        with pytest.raises(WrongAgentError):
            self.start_use_case.execute(ticket.id, wrong_agent)

    def test_start_ticket_persists_change(self):
        """Doit persister le démarrage dans le repository."""
        # Arrange
        ticket = self.create_use_case.execute(
            "Bug à corriger", "Description du bug", "user-123"
        )
        agent_id = "agent-456"
        self.assign_use_case.execute(ticket.id, agent_id)

        # Act
        self.start_use_case.execute(ticket.id, agent_id)

        # Assert - Récupérer depuis le repository
        persisted_ticket = self.repo.get_by_id(ticket.id)
        assert persisted_ticket.status == Status.IN_PROGRESS
        assert persisted_ticket.started_at == self.fixed_time

    def test_start_ticket_deterministic_with_fixed_clock(self):
        """Doit être déterministe avec FixedClock
        (même timestamp à chaque exécution)."""
        # Arrange - Créer plusieurs tickets
        agents = ["agent-1", "agent-2", "agent-3"]
        tickets = []

        for i, agent in enumerate(agents):
            ticket = self.create_use_case.execute(
                f"Bug {i}", f"Description {i}", "user-123"
            )
            self.assign_use_case.execute(ticket.id, agent)
            tickets.append(ticket)

        # Act - Démarrer tous les tickets
        started_tickets = []
        for ticket, agent in zip(tickets, agents):
            started = self.start_use_case.execute(ticket.id, agent)
            started_tickets.append(started)

        # Assert - Tous doivent avoir le même timestamp
        for started in started_tickets:
            assert started.started_at == self.fixed_time
