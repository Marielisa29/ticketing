from typing import Optional, List

from src.ports.user_repository import UserRepository
from src.domain.user import User
from .database import get_connection
from .mappers import user_to_row, row_to_user


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, user: User) -> User:
        """
        Insère ou remplace un utilisateur dans la table users.
        Utilise INSERT OR REPLACE pour permettre la création ou la mise à jour.
        """
        row = user_to_row(user)
        query = """
        INSERT OR REPLACE INTO users (id, username, is_agent, is_admin)
        VALUES (:id, :username, :is_agent, :is_admin)
        """
        with get_connection(self.db_path) as conn:
            conn.execute(query, row)
            conn.commit()
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Récupère un utilisateur par son id.
        """
        query = "SELECT id, username, is_agent, is_admin FROM users WHERE id = ?"
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(query, (user_id,))
            row = cursor.fetchone()
        if row is None:
            return None
        row_dict = {
            "id": row[0],
            "username": row[1],
            "is_agent": row[2],
            "is_admin": row[3],
        }
        return row_to_user(row_dict)

    def find_by_username(self, username: str) -> Optional[User]:
        """
        Recherche un utilisateur par son username.
        """
        query = "SELECT id, username, is_agent, is_admin FROM users WHERE username = ?"
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(query, (username,))
            row = cursor.fetchone()
        if row is None:
            return None
        row_dict = {
            "id": row[0],
            "username": row[1],
            "is_agent": row[2],
            "is_admin": row[3],
        }
        return row_to_user(row_dict)

    def list_all(self) -> List[User]:
        """
        Retourne tous les utilisateurs de la table users.
        """
        query = "SELECT id, username, is_agent, is_admin FROM users"
        users: List[User] = []
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
        for row in rows:
            row_dict = {
                "id": row[0],
                "username": row[1],
                "is_agent": row[2],
                "is_admin": row[3],
            }
            users.append(row_to_user(row_dict))
        return users