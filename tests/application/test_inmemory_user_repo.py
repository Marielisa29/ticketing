from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.domain.user import User


def test_inmemory_user_repo():
    repo = InMemoryUserRepository()
    user = User(id="u1", username="alice")

    repo.save(user)
    retrieved = repo.get_by_id("u1")

    assert retrieved is not None
    assert retrieved.username == "alice"
