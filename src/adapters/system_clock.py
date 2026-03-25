"""
Adaptateur production pour l'horodatage.

Utilise l'heure système réelle.
"""

from datetime import datetime, timezone

from src.ports.clock import Clock


class SystemClock(Clock):
    """
    Implémentation production du port Clock.

    Retourne l'heure système réelle en UTC.
    """

    def now(self) -> datetime:
        """
        Retourne l'heure système actuelle en UTC.

        Returns:
            datetime: L'instant présent en UTC
        """
        return datetime.now(timezone.utc)
