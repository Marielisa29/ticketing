"""
Adaptateur InMemory pour le repository de tickets.

Implémentation simple du TicketRepository qui stocke les tickets en mémoire.
Utilisé principalement pour les tests et le développement.
"""

from typing import Optional

from src.domain.ticket import Ticket
from src.ports.ticket_repository import TicketRepository


class InMemoryTicketRepository(TicketRepository):
    """
    Repository en mémoire utilisant un dictionnaire Python.
    
    Les données sont perdues à chaque redémarrage.
    Idéal pour les tests unitaires et l'apprentissage.
    """

    def __init__(self):
        """Initialise le repository avec un dictionnaire vide."""
        self._tickets: dict[str, Ticket] = {}

    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket dans le dictionnaire.
        
        Args:
            ticket: Le ticket à sauvegarder
            
        Returns:
            Le ticket sauvegardé
        """
        self._tickets[ticket.id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son ID.
        
        Args:
            ticket_id: L'identifiant du ticket
            
        Returns:
            Le ticket ou None
        """
        return self._tickets.get(ticket_id)

    def list_all(self) -> list[Ticket]:
        """
        Retourne tous les tickets stockés.
        
        Returns:
            Liste de tous les tickets
        """
        return list(self._tickets.values())

    def clear(self):
        """
        Vide le repository (utile pour les tests).
        
        Note: Cette méthode n'est pas dans le port, elle est spécifique
        à l'implémentation InMemory pour faciliter les tests.
        """
        self._tickets.clear()
