"""
Adaptateur test pour l'horodatage.

Retourne une heure fixe pour les tests (déterministe).
"""

from datetime import datetime

from src.ports.clock import Clock


class FixedClock(Clock):
    """
    Implémentation test du port Clock.

    Retourne toujours la même heure fixe (pour des tests déterministes).
    """

    def __init__(self, fixed_time: datetime):
        """
        Initialise l'horloge avec un temps fixe.

        Args:
            fixed_time: L'heure qui sera toujours retournée par now()
        """
        self.fixed_time = fixed_time

    def now(self) -> datetime:
        """
        Retourne l'heure fixe configurée.

        Returns:
            datetime: L'heure fixe (toujours la même)
        """
        return self.fixed_time
