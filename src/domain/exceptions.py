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
