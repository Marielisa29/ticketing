"""
Tests du use case AssignTicket.
"""

import pytest

from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.domain.exceptions import TicketNotFoundError


class TestAssignTicketUseCase:
    """Suite de tests pour l'assignation de tickets."""

    def setup_method(self):
        """Initialise le repository et les use cases."""
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.assign_use_case = AssignTicketUseCase(self.repo)

    def test_assign_ticket_success(self):
        """Doit assigner un ticket à un agent."""
        # Arrange - Créer un ticket d'abord
        ticket = self.create_use_case.execute(
            "Bug à corriger",
            "Description du bug",
            "user-123"
        )
        agent_id = "agent-456"

        # Act
        updated_ticket = self.assign_use_case.execute(ticket.id, agent_id)

        # Assert
        assert updated_ticket.assignee_id is not None
        assert updated_ticket.assignee_id == agent_id

    def test_assign_nonexistent_ticket_raises_error(self):
        """Doit lever une erreur si le ticket n'existe pas."""
        # Arrange
        fake_id = "ticket-inexistant"
        agent_id = "agent-789"

        # Act & Assert
        with pytest.raises(TicketNotFoundError):
            self.assign_use_case.execute(fake_id, agent_id)

    def test_assign_ticket_persists_change(self):
        """Doit persister l'assignation dans le repository."""
        # Arrange
        ticket = self.create_use_case.execute(
            "Bug persistance",
            "Vérifier que l'assignation est bien sauvegardée",
            "user-123"
        )
        agent_id = "agent-999"

        # Act
        self.assign_use_case.execute(ticket.id, agent_id)

        # Assert - Récupérer depuis le repo pour vérifier la persistance
        saved_ticket = self.repo.get_by_id(ticket.id)
        assert saved_ticket.assignee_id is not None
        assert saved_ticket.assignee_id == agent_id

    # --- Cas d'erreur ---

    def test_assign_closed_ticket_raises_error(self):
        """Doit lever une ValueError si le ticket est fermé."""
        # Arrange
        ticket = self.create_use_case.execute(
            "Bug fermé",
            "Ce ticket est déjà clôturé",
            "user-123"
        )
        ticket.close()
        self.repo.save(ticket)

        # Act & Assert
        with pytest.raises(ValueError):
            self.assign_use_case.execute(ticket.id, "agent-456")

    def test_assign_ticket_does_not_change_assignee_on_error(self):
        """L'assignee ne doit pas changer si l'assignation échoue."""
        # Arrange - ticket fermé sans assignee
        ticket = self.create_use_case.execute(
            "Bug fermé sans assignee",
            "Description",
            "user-123"
        )
        ticket.close()
        self.repo.save(ticket)

        # Act
        with pytest.raises(ValueError):
            self.assign_use_case.execute(ticket.id, "agent-456")

        # Assert - l'assignee reste None
        saved_ticket = self.repo.get_by_id(ticket.id)
        assert saved_ticket.assignee_id is None
