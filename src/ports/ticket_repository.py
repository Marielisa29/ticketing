"""
Port (interface) pour la persistance des tickets.
Ce module définit le contrat que tout adaptateur de stockage doit respecter.
Les use cases utilisent cette interface, sans connaître l'implémentation concrète.
"""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.ticket import Ticket


class TicketRepository(ABC):
    """
    Interface abstraite pour la persistance des tickets.

    Définit le contrat (port) que tout adaptateur de stockage doit respecter,
    qu'il s'agisse d'une implémentation en mémoire, SQLite, PostgreSQL, etc.

    Les use cases dépendent uniquement de cette interface — jamais d'une
    implémentation concrète. C'est le principe d'inversion de dépendances
    au cœur de l'architecture hexagonale.

    Toute nouvelle implémentation doit fournir les trois opérations définies
    ci-dessous : save, get_by_id et list_all.
    """

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket (création ou mise à jour).

        Si un ticket avec le même identifiant existe déjà, il doit être
        remplacé (comportement upsert). Sinon, le ticket est créé.

        Args:
            ticket: Le ticket à sauvegarder. Doit avoir un attribut `id` non vide.

        Returns:
            Le ticket tel qu'il a été persisté.
        """
        ...

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant unique.

        Args:
            ticket_id: L'identifiant unique du ticket recherché.

        Returns:
            Le ticket correspondant à l'identifiant,
            ou None si aucun ticket ne correspond.
        """
        ...

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        """
        Récupère tous les tickets du système.

        Returns:
            Liste de tous les tickets persistés.
            Retourne une liste vide si aucun ticket n'existe.
        """
        ...
