"""
Racine de composition (Composition Root).

Ce fichier est le point d'entrée de l'application. C'est ici que :
- Les adaptateurs concrets sont instanciés
- Les dépendances sont injectées dans les cas d'usage
- L'application FastAPI est configurée avec ses routes

La règle d'or : seul ce fichier connaît les implémentations concrètes.
Les cas d'usage ne voient que les interfaces (ports).
"""

from fastapi import FastAPI

from src.adapters.api.ticket_router import router as ticket_router
from src.adapters.api.user_router import router as user_router
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.adapters.db.user_repository_inmemory import InMemoryUserRepository
from src.application.usecases.assign_ticket import AssignTicketUseCase
from src.application.usecases.create_ticket import CreateTicketUseCase
from src.application.usecases.create_user import CreateUserUseCase
from src.application.usecases.list_ticket import ListTicketsUseCase
from src.application.usecases.list_user import ListUsersUseCase
from src.application.usecases.start_ticket import StartTicketUseCase
from src.ports import clock

app = FastAPI(title="Ticketing Starter")

# --- Configuration de l'injection de dépendances ---
# Création des instances d'adaptateurs (instance unique partagée entre les requêtes)
ticket_repository = InMemoryTicketRepository()
user_repository = InMemoryUserRepository()


# Fonctions factory pour les cas d'usage (FastAPI les appellera via Depends)
def get_create_ticket_usecase() -> CreateTicketUseCase:
    """
    Factory pour le cas d'usage CreateTicket.

    Returns:
        Une instance de CreateTicketUseCase avec le repository injecté
    """
    return CreateTicketUseCase(ticket_repository)


def get_list_tickets_usecase() -> ListTicketsUseCase:
    return ListTicketsUseCase(ticket_repository)


def get_assign_ticket_usecase() -> AssignTicketUseCase:
    return AssignTicketUseCase(ticket_repository)


def get_create_user_usecase() -> CreateUserUseCase:
    return CreateUserUseCase(user_repository)


def get_list_users_usecase() -> ListUsersUseCase:
    return ListUsersUseCase(user_repository)


def get_start_ticket_usecase() -> StartTicketUseCase:
    return StartTicketUseCase(ticket_repository=ticket_repository, clock=clock)


# --- Routes ---
app.include_router(ticket_router)
app.include_router(user_router)


@app.get("/")
def root():
    """Route racine pour vérifier que l'API fonctionne."""
    return {"status": "ok"}
