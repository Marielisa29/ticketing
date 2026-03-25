"""
Exceptions du domaine métier.

Ce module contient les exceptions spécifiques au domaine.
Utilisez ces exceptions pour signaler des violations de règles métier.
"""


class DomainError(Exception):
    """
    Exception de base pour toutes les erreurs du domaine.

    Héritez de cette classe pour créer des exceptions métier spécifiques.
    Exemple: TicketNotFoundError, InvalidStatusTransitionError, etc.
    """

    pass


class TicketNotFoundError(DomainError):
    """
    Levée quand un ticket demandé n'existe pas.
    """

    pass


class TicketNotAssignedError(DomainError):
    """Levée quand on essaie de démarrer un ticket non assigné."""

    pass


class WrongAgentError(DomainError):
    """Levée quand un agent essaie de démarrer un ticket assigné à quelqu'un d'autre."""

    pass


class InvalidTicketStateError(DomainError):
    """Levée quand on essaie une opération invalide pour l'état actuel du ticket."""

    pass
