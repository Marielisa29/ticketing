"""
Port (interface) pour l'horodatage.

Ce module définit le contrat que tout adaptateur de temps doit respecter.
Les use cases utilisent cette interface pour obtenir l'heure,
sans dépendre d'une implémentation concrète.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """
    Interface abstraite pour l'horodatage.

    Cette interface permet aux use cases et aux entités du domaine
    d'obtenir l'heure sans dépendre du système (testabilité).
    """

    @abstractmethod
    def now(self) -> datetime:
        """
        Retourne la date/heure actuelle.

        Returns:
            Un objet datetime représentant l'instant présent
        """
        ...
