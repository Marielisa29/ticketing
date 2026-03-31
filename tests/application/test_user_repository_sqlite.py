"""
Tests du repository SQLite pour les utilisateurs.

Ces tests vérifient l'adaptateur SQLite en isolation.
"""

from src.domain.user import User


class TestSQLiteUserRepository:
    """Suite de tests pour le SQLiteUserRepository."""

    def test_save_and_retrieve_user(self, sqlite_user_repo):
        """Doit sauvegarder et récupérer un utilisateur."""
        user = User(id="user-1", username="alice", is_agent=True, is_admin=False)
        
        saved = sqlite_user_repo.save(user)
        assert saved.id == "user-1"
        
        retrieved = sqlite_user_repo.get_by_id("user-1")
        assert retrieved is not None
        assert retrieved.username == "alice"
        assert retrieved.is_agent is True

    def test_find_by_username(self, sqlite_user_repo):
        """Doit trouver un utilisateur par username."""
        user = User(id="user-2", username="bob_agent", is_agent=True)
        sqlite_user_repo.save(user)
        
        found = sqlite_user_repo.find_by_username("bob_agent")
        assert found is not None
        assert found.id == "user-2"
        
    def test_find_by_username_returns_none_when_not_found(self, sqlite_user_repo):
        """Doit retourner None si username introuvable."""
        result = sqlite_user_repo.find_by_username("nonexistent")
        assert result is None

    def test_list_all_returns_all_users(self, sqlite_user_repo):
        """Doit lister tous les utilisateurs."""
        user1 = User(id="u1", username="charlie", is_agent=False)
        user2 = User(id="u2", username="diane_admin", is_agent=True, is_admin=True)
        
        sqlite_user_repo.save(user1)
        sqlite_user_repo.save(user2)
        
        all_users = sqlite_user_repo.list_all()
        assert len(all_users) == 2