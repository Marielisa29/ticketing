"""
Adaptateur API REST pour les utilisateurs.

Ce module définit les routes HTTP pour manipuler les utilisateurs.
C'est un adaptateur "primaire" (ou "driving") : il reçoit les requêtes
de l'extérieur et appelle les cas d'usage de l'application.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])


class UserIn(BaseModel):
    """
    Schéma d'entrée pour la création d'un utilisateur.

    Attributes:
        username: Nom d'utilisateur unique
        is_agent: Si l'utilisateur peut traiter des tickets
        is_admin: Si l'utilisateur a des droits administrateur
    """

    username: str
    is_agent: bool = False
    is_admin: bool = False


class UserOut(BaseModel):
    """
    Schéma de sortie pour un utilisateur.

    Attributes:
        id: Identifiant unique de l'utilisateur
        username: Nom d'utilisateur
        is_agent: Si l'utilisateur peut traiter des tickets
        is_admin: Si l'utilisateur a des droits administrateur
    """

    id: str
    username: str
    is_agent: bool
    is_admin: bool


@router.post("/", status_code=201, response_model=UserOut)
async def create_user(payload: UserIn):
    """
    Crée un nouvel utilisateur.

    Args:
        payload: Les données de l'utilisateur à créer

    Returns:
        L'utilisateur créé avec son identifiant

    Raises:
        HTTPException 400: Si le username existe déjà
    """
    from src.main import get_create_user_usecase

    usecase = get_create_user_usecase()
    try:
        user = usecase.execute(
            username=payload.username,
            is_agent=payload.is_agent,
            is_admin=payload.is_admin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return UserOut(
        id=user.id,
        username=user.username,
        is_agent=user.is_agent,
        is_admin=user.is_admin,
    )


@router.get("/", response_model=list[UserOut])
async def list_users():
    """
    Liste tous les utilisateurs.

    Returns:
        Liste de tous les utilisateurs existants
    """
    from src.main import get_list_users_usecase

    usecase = get_list_users_usecase()
    users = usecase.execute()
    return [
        UserOut(
            id=user.id,
            username=user.username,
            is_agent=user.is_agent,
            is_admin=user.is_admin,
        )
        for user in users
    ]
