from typing import Optional

from src.domain.user import User
from src.ports.user_repository import UserRepository


class GetUserByUsernameUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, username: str) -> Optional[User]:
        return self.user_repo.find_by_username(username)
