"""
Entité User (utilisateur du système).

TODO (TD01) : Compléter cette classe avec les attributs nécessaires.
"""

from dataclasses import dataclass


@dataclass
class User:
    """
    Représente un utilisateur du système de ticketing.

    TODO: Définir les attributs nécessaires.
    Réfléchissez aux informations minimales pour identifier un utilisateur
    et distinguer ses rôles (simple utilisateur, agent support, admin...).

    Attributes:
        id: Identifiant unique de l'utilisateur
        # TODO: Ajouter d'autres attributs
    """

    id: str
    # TODO: Compléter avec les attributs manquants
    # - username ?
    # - is_agent ? is_admin ?
