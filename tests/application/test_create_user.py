"""
Tests du use case CreateUser.

Ces tests vérifient que le use case orchestre correctement
le domaine et le repository.
"""

import pytest

from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.application.usecases.create_user import CreateUserUseCase


class TestCreateUserUseCase:
    """Suite de tests pour la création d'utilisateurs."""

    def setup_method(self):
        """Initialise le repository et le use case avant chaque test."""
        self.repo = InMemoryUserRepository()
        self.use_case = CreateUserUseCase(self.repo)

    def test_create_user_success(self):
        """Doit créer un utilisateur avec les bonnes propriétés."""
        username = "alice"
        
        user = self.use_case.execute(username)
        
        assert user.id is not None
        assert user.username == username
        assert user.is_agent is False
        assert user.is_admin is False

    def test_create_agent_user(self):
        """Doit créer un utilisateur agent."""
        user = self.use_case.execute("bob_agent", is_agent=True)
        
        assert user.is_agent is True
        assert user.is_admin is False

    def test_create_user_with_duplicate_username_raises_error(self):
        """Doit lever une erreur si le username existe déjà."""
        username = "duplicate_user"
        self.use_case.execute(username)
        
        with pytest.raises(ValueError, match="already exists"):
            self.use_case.execute(username)