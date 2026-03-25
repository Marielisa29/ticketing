import pytest

from src.adapters.db.database import init_database
from src.adapters.db.ticket_repository_sqlite import SQLiteTicketRepository


@pytest.fixture
def sqlite_ticket_repo(tmp_path):
    """
    Fixture fournissant un repository SQLite de tickets avec une base de données temporaire.

    Crée une base de données fraîche et isolée pour chaque test afin de garantir
    l'indépendance des tests. La base de données est automatiquement nettoyée
    après le test par pytest.

    Args:
        tmp_path: Répertoire temporaire fourni par pytest (auto-nettoyage)

    Returns:
        SQLiteTicketRepository: Instance du repository avec base de données temporaire

    Exemple:
        def test_save_ticket(sqlite_ticket_repo):
            ticket = Ticket(...)
            sqlite_ticket_repo.save(ticket)
            assert sqlite_ticket_repo.get_by_id(ticket.id) is not None
    """
    # Création d'un fichier de base de données dans le répertoire temporaire
    db_path = tmp_path / "test.db"

    # Initialisation de la base de données avec le schéma
    init_database(str(db_path))

    # Création et retour du repository
    repo = SQLiteTicketRepository(str(db_path))
    return repo
    # Pas de nettoyage nécessaire : pytest supprime automatiquement tmp_path après le test
