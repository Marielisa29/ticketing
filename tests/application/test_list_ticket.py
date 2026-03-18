"""
Tests du use case ListTickets.
"""

from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.list_ticket import ListTicketsUseCase
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.domain.status import Status


class TestListTicketsUseCase:
    """Suite de tests pour la liste des tickets."""

    def setup_method(self):
        """Initialise le repository et les use cases."""
        self.repo = InMemoryTicketRepository()
        self.create_use_case = CreateTicketUseCase(self.repo)
        self.list_use_case = ListTicketsUseCase(self.repo)

    def test_list_all_tickets(self):
        """Doit retourner tous les tickets sans filtre."""
        # Arrange
        self.create_use_case.execute("Bug 1", "Description 1", "user-1")
        self.create_use_case.execute("Bug 2", "Description 2", "user-2")
        self.create_use_case.execute("Bug 3", "Description 3", "user-3")

        # Act
        tickets = self.list_use_case.execute()

        # Assert
        assert len(tickets) == 3

    def test_list_empty_repository(self):
        """Doit retourner une liste vide si aucun ticket n'existe."""
        # Act
        tickets = self.list_use_case.execute()

        # Assert
        assert tickets == []

    def test_list_tickets_filtered_by_status(self):
        """Doit retourner uniquement les tickets du statut demandé."""
        # Arrange
        self.create_use_case.execute("Bug open 1", "Description 1", "user-1")
        self.create_use_case.execute("Bug open 2", "Description 2", "user-2")
        ticket_to_close = self.create_use_case.execute("Bug à clore", "Description 3", "user-3")
        ticket_to_close.close()
        self.repo.save(ticket_to_close)

        # Act
        open_tickets = self.list_use_case.execute(status=Status.OPEN)
        closed_tickets = self.list_use_case.execute(status=Status.CLOSED)

        # Assert
        assert len(open_tickets) == 2
        assert len(closed_tickets) == 1
        assert all(t.status == Status.OPEN for t in open_tickets)
        assert all(t.status == Status.CLOSED for t in closed_tickets)

    # --- Cas d'erreur ---

    def test_list_tickets_filter_no_match_returns_empty(self):
        """Doit retourner une liste vide si aucun ticket ne correspond au filtre."""
        # Arrange - uniquement des tickets OPEN
        self.create_use_case.execute("Bug 1", "Description 1", "user-1")
        self.create_use_case.execute("Bug 2", "Description 2", "user-2")

        # Act
        closed_tickets = self.list_use_case.execute(status=Status.CLOSED)

        # Assert
        assert closed_tickets == []

    def test_list_tickets_filter_does_not_mutate_repository(self):
        """Filtrer les tickets ne doit pas modifier le repository."""
        # Arrange
        self.create_use_case.execute("Bug 1", "Description 1", "user-1")
        self.create_use_case.execute("Bug 2", "Description 2", "user-2")

        # Act - filtre qui ne retourne rien
        self.list_use_case.execute(status=Status.CLOSED)

        # Assert - le repo contient toujours tous les tickets
        assert len(self.repo.list_all()) == 2
