"""
Tests pour les cas d'usage (TD2).

Ces tests vérifient la logique applicative.
Ils utilisent des adaptateurs "fake" (InMemory) pour isoler les tests.

Écrivez vos tests ici après avoir terminé TD1.
Lancez-les avec : pytest tests/application/
"""

# TODO (TD2): Décommenter ces imports une fois le domaine implémenté
# from src.adapters.db.ticket_repository_inmemory import InMemoryTicketRepository
# from src.application.usecases.create_ticket import CreateTicketUseCase


# ==========================================================================
# EXEMPLES DE TESTS À ÉCRIRE (décommentez et adaptez)
# ==========================================================================

# def test_create_ticket_success():
#     """Vérifie la création d'un ticket via le use case."""
#     repo = InMemoryTicketRepository()
#     usecase = CreateTicketUseCase(repo)
#
#     ticket = usecase.execute(
#         title="Problème d'affichage",
#         description="L'écran reste noir",
#         creator_id="user123",
#     )
#
#     assert ticket.id is not None
#     assert repo.get(ticket.id) is not None


# def test_create_ticket_is_persisted():
#     """Vérifie que le ticket créé peut être récupéré."""
#     repo = InMemoryTicketRepository()
#     usecase = CreateTicketUseCase(repo)
#
#     ticket = usecase.execute("Test", "Description", "user1")
#     retrieved = repo.get(ticket.id)
#
#     assert retrieved is not None
#     assert retrieved.creator_id == "user1"


# ==========================================================================
# AUTRES TESTS À ÉCRIRE
# ==========================================================================

# def test_list_tickets_usecase():
#     """Vérifie la récupération de tous les tickets."""
#     # TODO: Implémenter ListTicketsUseCase et son test
#     pass


# def test_assign_ticket_usecase():
#     """Vérifie l'assignation d'un ticket via use case."""
#     # TODO: Implémenter AssignTicketUseCase et son test
#     pass
