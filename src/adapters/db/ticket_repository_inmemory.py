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

    Implémentation concrète du port TicketRepository qui stocke les tickets
    dans un dictionnaire {id: ticket}. Les données sont perdues à chaque
    redémarrage de l'application.

    Utilisée exclusivement pour les tests et le développement local.
    Ne doit jamais être utilisée en production.
    """

    def __init__(self):
        """
        Initialise le repository avec un dictionnaire vide.

        Le dictionnaire interne `_tickets` est préfixé par `_` pour signaler
        qu'il s'agit d'un détail d'implémentation privé, non accessible
        directement depuis l'extérieur.
        """
        self._tickets: dict[str, Ticket] = {}

    def save(self, ticket: Ticket) -> Ticket:
        """
        Sauvegarde un ticket dans le dictionnaire (création ou mise à jour).

        Utilise l'identifiant du ticket comme clé. Si un ticket avec le même
        identifiant existe déjà, il est écrasé (comportement upsert).

        Args:
            ticket: Le ticket à sauvegarder. Doit avoir un attribut `id` non vide.

        Returns:
            Le ticket tel qu'il a été stocké (même référence que l'entrée).
        """
        self._tickets[ticket.id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère un ticket par son identifiant unique.

        Args:
            ticket_id: L'identifiant du ticket recherché.

        Returns:
            Le ticket correspondant à l'identifiant,
            ou None si aucun ticket ne correspond.
        """
        return self._tickets.get(ticket_id)

    def list_all(self) -> list[Ticket]:
        """
        Retourne tous les tickets stockés dans le repository.

        Retourne une copie de la liste (pas une vue directe sur le dictionnaire)
        pour éviter les modifications accidentelles de l'état interne.

        Returns:
            Liste de tous les tickets dans l'ordre d'insertion.
            Retourne une liste vide si le repository ne contient aucun ticket.
        """
        return list(self._tickets.values())

    def clear(self):
        """
        Vide intégralement le repository.

        Supprime tous les tickets stockés. Utile dans les tests pour
        garantir un état propre entre deux scénarios (alternative à
        réinstancier un nouveau repository).

        Note:
            Cette méthode n'est pas définie dans le port TicketRepository.
            Elle est spécifique à cette implémentation InMemory et ne doit
            pas être appelée depuis un use case (qui ne connaît que le port).
        """
        self._tickets.clear()
