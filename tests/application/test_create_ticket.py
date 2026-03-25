"""
Tests du use case CreateTicket.

Ces tests vérifient que le use case orchestre correctement
le domaine et le repository.
"""

from pathlib import Path

import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository
from src.application.usecases.create_ticket import CreateTicketUseCase
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

    # --- Cas d'erreur ---

    def test_create_ticket_empty_title_raises_error(self):
        """Doit lever une ValueError si le titre est vide."""
        # Act & Assert
        with pytest.raises(ValueError):
            self.use_case.execute("", "Description valide", "user-123")

    def test_create_ticket_empty_description_raises_error(self):
        """Doit lever une ValueError si la description est vide."""
        # Act & Assert
        with pytest.raises(ValueError):
            self.use_case.execute("Titre valide", "", "user-123")

    def test_create_ticket_not_persisted_on_error(self):
        """Le repository ne doit pas contenir de ticket si la création échoue."""
        # Act
        with pytest.raises(ValueError):
            self.use_case.execute("", "Description valide", "user-123")

        # Assert - Aucun ticket sauvegardé
        assert self.repo.list_all() == []

    def test_create_ticket_with_sqlite(self, tmp_path: Path):
        """Doit créer un ticket et le persister dans SQLite (intégration minimale)."""
        db_file = tmp_path / "test_create_ticket.db"
        db_path_str = str(db_file)

        # Initialise la base (si vous possédez schema.sql et init_database)
        # Si vous n'avez pas init_database, assurez-vous que la table 'tickets' existe.
        init_database(db_path=db_path_str)

        sqlite_repo = SQLiteTicketRepository(db_path=db_path_str)
        use_case = CreateTicketUseCase(sqlite_repo)

        title = "Bug critique"
        description = "Le système plante"
        creator_id = "user-sqlite"

        ticket = use_case.execute(title, description, creator_id)

        assert ticket.id is not None
        assert ticket.status == Status.OPEN

        # Vérifier persistance : récupérer depuis la DB
        retrieved = sqlite_repo.get_by_id(ticket.id)
        assert retrieved is not None
        assert retrieved.title == title
        assert retrieved.creator_id == creator_id
