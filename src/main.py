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
from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
from src.application.usecases.create_ticket import CreateTicketUseCase

app = FastAPI(title="Ticketing Starter")

# --- Configuration de l'injection de dépendances ---
# Création des instances d'adaptateurs (instance unique partagée entre les requêtes)
ticket_repository = InMemoryTicketRepository()


# Fonctions factory pour les cas d'usage (FastAPI les appellera via Depends)
def get_create_ticket_usecase() -> CreateTicketUseCase:
    """
    Factory pour le cas d'usage CreateTicket.

    Returns:
        Une instance de CreateTicketUseCase avec le repository injecté
    """
    return CreateTicketUseCase(ticket_repository)


# TODO: Ajouter d'autres factories de cas d'usage au fur et à mesure
# def get_assign_ticket_usecase() -> AssignTicketUseCase:
#     return AssignTicketUseCase(ticket_repository)

# --- Routes ---
app.include_router(ticket_router)


@app.get("/")
def root():
    """Route racine pour vérifier que l'API fonctionne."""
    return {"status": "ok"}
