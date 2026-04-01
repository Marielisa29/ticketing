"""Use case : Lister tous les utilisateurs."""

from src.domain.user import User
from src.ports.user_repository import UserRepository


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self) -> list[User]:
        return self.user_repository.list_all()
