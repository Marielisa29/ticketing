"""
Port (interface) pour la persistance des tickets.

Ce module définit le contrat que tout adaptateur de stockage doit respecter.
Le domaine et l'application utilisent cette interface, sans connaître
l'implémentation concrète (mémoire, SQLite, PostgreSQL, etc.).
"""

from abc import ABC, abstractmethod

# TODO: Décommenter une fois la classe Ticket implémentée (TD01)
# from src.domain.ticket import Ticket
# Placeholder temporaire pour éviter les erreurs d'import
from typing import Any, List, Optional

Ticket = Any  # À supprimer après TD01


class TicketRepository(ABC):
    """
    Interface abstraite pour le repository de tickets.

    Cette classe définit les opérations de base (CRUD) sur les tickets.
    Les adaptateurs concrets (InMemory, SQLite, etc.) doivent implémenter
    toutes ces méthodes.
    """

    @abstractmethod
    def save(self, ticket: Ticket) -> None:
        """
        Sauvegarde un ticket (création ou mise à jour).

        Args:
            ticket: Le ticket à sauvegarder
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant.

        Args:
            ticket_id: L'identifiant unique du ticket

        Returns:
            Le ticket trouvé, ou None s'il n'existe pas
        """
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Ticket]:
        """
        Récupère tous les tickets.

        Returns:
            Liste de tous les tickets
        """
        raise NotImplementedError
