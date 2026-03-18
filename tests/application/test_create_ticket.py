"""
Tests du use case CreateTicket.

Ces tests vérifient que le use case orchestre correctement
le domaine et le repository.
"""

import pytest

from src.application.usecases.create_ticket import CreateTicketUseCase
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.domain.status import Status


class TestCreateTicketUseCase:
    """Suite de tests pour la création de tickets."""

    def setup_method(self):
        """Initialise le repository et le use case avant chaque test."""
        self.repo = InMemoryTicketRepository()
        self.use_case = CreateTicketUseCase(self.repo)

    def test_create_ticket_success(self):
        """Doit créer un ticket avec les bonnes propriétés."""
        # Arrange
        title = "Bug critique"
        description = "L'application plante au démarrage"
        creator_id = "user-123"

        # Act
        ticket = self.use_case.execute(title, description, creator_id)

        # Assert
        assert ticket.id is not None
        assert ticket.title == title
        assert ticket.description == description
        assert ticket.status == Status.OPEN
        assert ticket.creator_id == creator_id
        assert ticket.assignee_id is None

    def test_create_ticket_persists_in_repository(self):
        """Doit sauvegarder le ticket dans le repository."""
        # Arrange
        title = "Nouvelle fonctionnalité"
        description = "Ajouter un bouton export"
        creator_id = "user-456"

        # Act
        ticket = self.use_case.execute(title, description, creator_id)

        # Assert - Vérifier que le ticket est bien dans le repository
        saved_ticket = self.repo.get_by_id(ticket.id)
        assert saved_ticket is not None
        assert saved_ticket.id == ticket.id
        assert saved_ticket.title == title

    def test_create_multiple_tickets(self):
        """Doit pouvoir créer plusieurs tickets distincts."""
        # Arrange & Act
        ticket1 = self.use_case.execute("Bug 1", "Description 1", "user-1")
        ticket2 = self.use_case.execute("Bug 2", "Description 2", "user-2")

        # Assert
        assert ticket1.id != ticket2.id
        all_tickets = self.repo.list_all()
        assert len(all_tickets) == 2
