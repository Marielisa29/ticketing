from enum import Enum

class Priority(Enum):
    """
    Définition des priorités tickets.
    """

    LOW = "Basse"
    MEDIUM = "Moyenne"
    HIGH = "Elevée"
    CRITICAL = "Critique"

    def __str__(self):
        return self.value