"""
Adaptateur InMemory pour le repository d'utilisateurs.
"""

from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """Repository en mémoire pour les tests rapides."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def save(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def list_all(self) -> list[User]:
        return list(self._users.values())

    def find_agents(self) -> list[User]:
        return [u for u in self._users.values() if u.is_agent]

    def clear(self):
        self._users.clear()
