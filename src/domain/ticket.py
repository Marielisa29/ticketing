"""
Entité Ticket (ticket de support).

TODO (TD01) : Compléter cette classe avec les attributs et méthodes nécessaires.
C'est l'entité centrale du domaine métier.
"""

from dataclasses import dataclass
from datetime import datetime, timezone


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    """
    Entité principale du domaine : un ticket de support.

    TODO: Compléter cette classe avec :
    1. Les attributs obligatoires (id, title, description, status...)
    2. Les attributs optionnels (assignee, dates...)
    3. Les méthodes métier (assign, close...)

    Pensez aux règles métier (invariants) :
    - Un ticket doit avoir un titre non vide
    - Un ticket fermé ne peut plus être modifié
    - etc.

    Attributs:
        id: Identifiant unique du ticket
        title: Titre court décrivant le problème
        description: Description détaillée
        # TODO: Ajouter les autres attributs
    """

    id: str
    title: str
    description: str
    # TODO: Ajouter les attributs manquants
    # - status (avec valeur par défaut Status.OPEN)
    # - creator_id
    # - assignee_id (optionnel)
    # - created_at, updated_at (dates)

    # TODO: Ajouter les méthodes métier
    # def assign(self, user_id: str):
    #     """Assigne le ticket à un agent."""
    #     pass
    #
    # def close(self):
    #     """Ferme le ticket."""
    #     pass
