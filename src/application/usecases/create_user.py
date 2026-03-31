"""
Use case : Créer un utilisateur.

Ce use case orchestre la création d'un utilisateur en utilisant les entités du domaine
et le port UserRepository, sans dépendre d'une implémentation concrète.
"""

import uuid

from src.domain.user import User
from src.ports.user_repository import UserRepository


class CreateUserUseCase:
    """
    Cas d'usage pour créer un nouvel utilisateur.

    Reçoit le repository via injection de dépendances (principe d'inversion).
    """

    def __init__(self, user_repo: UserRepository):
        """
        Initialise le use case avec ses dépendances.

        Args:
            user_repo: Le repository (via son interface)
        """
        self.user_repo = user_repo

    def execute(
        self, username: str, is_agent: bool = False, is_admin: bool = False
    ) -> User:
        """
        Exécute la création d'un utilisateur.

        Args:
            username: Nom d'utilisateur
            is_agent: Si l'utilisateur peut gérer des tickets
            is_admin: Si l'utilisateur a les droits admin

        Returns:
            L'utilisateur créé

        Raises:
            ValueError: Si les données sont invalides ou si le username existe déjà
        """
        # Vérifier que le username n'existe pas déjà
        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            raise ValueError(f"Username '{username}' already exists")

        # Générer un ID unique
        user_id = str(uuid.uuid4())

        # Créer l'entité User (la validation se fait dans __post_init__)
        user = User(id=user_id, username=username, is_agent=is_agent, is_admin=is_admin)

        # Persister via le repository
        self.user_repo.save(user)

        return user
