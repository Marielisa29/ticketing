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


class TestSQLiteUserRepositoryFindAgents:
    """Tests de la méthode find_agents."""

    def test_find_agents_returns_only_agents(self, sqlite_user_repo):
        """Doit retourner uniquement les utilisateurs agents."""
        user1 = User(id="u1", username="alice", is_agent=False)
        user2 = User(id="u2", username="bob", is_agent=True)
        user3 = User(id="u3", username="charlie", is_agent=True)

        sqlite_user_repo.save(user1)
        sqlite_user_repo.save(user2)
        sqlite_user_repo.save(user3)

        agents = sqlite_user_repo.find_agents()

        assert len(agents) == 2
        usernames = [u.username for u in agents]

        assert "bob" in usernames
        assert "charlie" in usernames
        assert "alice" not in usernames

    def test_find_agents_returns_empty_list_when_no_agents(self, sqlite_user_repo):
        """Doit retourner une liste vide s'il n'y a aucun agent."""
        user1 = User(id="u1", username="alice", is_agent=False)
        sqlite_user_repo.save(user1)

        agents = sqlite_user_repo.find_agents()

        assert agents == []

    def test_find_agents_returns_all_when_all_are_agents(self, sqlite_user_repo):
        """Doit retourner tous les utilisateurs si tous sont agents."""
        user1 = User(id="u1", username="alice", is_agent=True)
        user2 = User(id="u2", username="bob", is_agent=True)

        sqlite_user_repo.save(user1)
        sqlite_user_repo.save(user2)

        agents = sqlite_user_repo.find_agents()

        assert len(agents) == 2
