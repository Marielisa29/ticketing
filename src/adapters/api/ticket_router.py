"""
Adaptateur API REST pour les tickets.

Ce module définit les routes HTTP pour manipuler les tickets.
C'est un adaptateur "primaire" (ou "driving") : il reçoit les requêtes
de l'extérieur et appelle les cas d'usage de l'application.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/tickets", tags=["tickets"])


class TicketIn(BaseModel):
    """
    Schéma d'entrée pour la création d'un ticket.

    Attributes:
        title: Titre du ticket
        description: Description détaillée du problème
    """

    title: str
    description: str


class TicketOut(BaseModel):
    """
    Schéma de sortie pour un ticket.

    Attributes:
        id: Identifiant unique du ticket
        title: Titre du ticket
        description: Description du problème
        status: Statut actuel (open, in_progress, resolved, closed)
    """

    id: str
    title: str
    description: str
    status: str


# Import de la factory du cas d'usage depuis la racine de composition
# Ceci évite les imports circulaires et garde l'injection de dépendances propre
def get_create_ticket_usecase():
    """
    Factory pour obtenir le cas d'usage CreateTicket.

    Cette fonction sera surchargée par la vraie factory dans main.py
    via app.dependency_overrides ou un pattern d'import direct.
    """
    from src.main import get_create_ticket_usecase as factory

    return factory()


@router.post("/", status_code=201, response_model=TicketOut)
async def create_ticket(
    payload: TicketIn,
    # TODO: Ajouter creator_id depuis le contexte d'authentification
):
    """
    Crée un nouveau ticket.

    Args:
        payload: Les données du ticket à créer

    Returns:
        Le ticket créé avec son identifiant et son statut
    """
    # Exemple de câblage (les étudiants complèteront ceci) :
    # usecase = get_create_ticket_usecase()
    # ticket = usecase.execute(
    #     payload.title, payload.description, creator_id="anonymous"
    # )
    # return TicketOut(
    #     id=ticket.id, title=ticket.title,
    #     description=ticket.description, status=ticket.status.value
    # )

    return TicketOut(
        id="TODO", title=payload.title, description=payload.description, status="open"
    )


@router.get("/")
async def list_tickets():
    """
    Liste tous les tickets.

    Returns:
        Liste des tickets existants
    """
    # TODO: appeler le cas d'usage ListTickets
    return []
