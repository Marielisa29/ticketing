from datetime import datetime

import pytest

from src.domain.utils import calculate_duration_hours


def test_calculate_duration_same_day():
    """Test avec deux dates le même jour."""
    start = datetime(2025, 1, 1, 9, 0)  # 1er janvier à 9h
    end = datetime(2025, 1, 1, 17, 0)  # 1er janvier à 17h

    result = calculate_duration_hours(start, end)

    assert result == 8.0  # 8 heures de différence


def test_calculate_duration_with_minutes():
    """Test avec des minutes (résultat décimal)."""
    start = datetime(2025, 1, 1, 10, 0)
    end = datetime(2025, 1, 1, 11, 30)

    result = calculate_duration_hours(start, end)

    assert result == 1.5  # 1h30 = 1.5 heures


def test_calculate_duration_invalid_order():
    """Test que la fonction lève une erreur si end < start."""
    start = datetime(2025, 1, 2, 9, 0)
    end = datetime(2025, 1, 1, 9, 0)  # Date de fin AVANT la date de début

    # On vérifie qu'une ValueError est levée
    with pytest.raises(ValueError):
        calculate_duration_hours(start, end)
