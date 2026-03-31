from abc import ABC, abstractmethod
from typing import Optional

from src.domain.user import User


class UserRepository(ABC):
    """
    Port pour la persistance des utilisateurs.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """Sauvegarde un utilisateur (création ou mise à jour)."""
        ...

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Récupère un utilisateur par son ID."""
        ...

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """Recherche un utilisateur par username."""
        ...

    @abstractmethod
    def list_all(self) -> list[User]:
        """Retourne tous les utilisateurs."""
        ...
