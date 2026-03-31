from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.domain.user import User


def test_inmemory_user_repo():
    repo = InMemoryUserRepository()
    user = User(id="u1", username="alice")

    repo.save(user)
    retrieved = repo.get_by_id("u1")

    assert retrieved is not None
    assert retrieved.username == "alice"


class TestInMemoryUserRepositoryFindAgents:
    def setup_method(self):
        self.repo = InMemoryUserRepository()

    def test_find_agents_returns_only_agents(self):
        user1 = User(id="u1", username="alice", is_agent=False)
        user2 = User(id="u2", username="bob", is_agent=True)

        self.repo.save(user1)
        self.repo.save(user2)

        agents = self.repo.find_agents()

        assert len(agents) == 1
        assert agents[0].username == "bob"

    def test_find_agents_empty(self):
        agents = self.repo.find_agents()
        assert agents == []
