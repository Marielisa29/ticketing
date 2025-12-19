from datetime import datetime

def calculate_duration_hours(start: datetime, end: datetime) -> float:
    """
    Calcule la durée en heures entre deux dates.

    Args:
        start: Date de début
        end: Date de fin

    Returns:
        Durée en heures (nombre décimal)

    Raises:
        ValueError: Si la date de fin est antérieure à la date de début

    Examples:
        >>> from datetime import datetime
        >>> start = datetime(2025, 1, 1, 9, 0)
        >>> end = datetime(2025, 1, 1, 17, 0)
        >>> calculate_duration_hours(start, end)
        8.0
    """
   
    if end < start:
        raise ValueError("Message d'erreur")

    delta = end - start
    heures = delta.total_seconds() / 3600

    return heures
