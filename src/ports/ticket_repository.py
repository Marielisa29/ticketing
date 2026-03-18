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
    
    Cette interface définit les opérations de base (CRUD) sur les tickets.
    Les adaptateurs concrets (InMemory, SQLite, etc.) implémenteront ces méthodes.
    """

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket (création ou mise à jour).
        
        Args:
            ticket: Le ticket à sauvegarder
            
        Returns:
            Le ticket sauvegardé (avec éventuellement un ID généré)
        """
        ...

    @abstractmethod
    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant.
        
        Args:
            ticket_id: L'identifiant unique du ticket
            
        Returns:
            Le ticket trouvé, ou None s'il n'existe pas
        """
        ...

    @abstractmethod
    def list_all(self) -> list[Ticket]:
        """
        Récupère tous les tickets du système.
        
        Returns:
            Liste de tous les tickets (peut être vide)
        """
        ...
