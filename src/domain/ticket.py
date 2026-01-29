from dataclasses import dataclass
from datetime import datetime, timezone

from src.domain.status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    creator_id: str
    status: Status = Status.OPEN
    assignee_id: str = None
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

    def assign(self, user_id: str):
        if self.status == Status.CLOSED:
            raise ValueError("Cannot assign a closed ticket")
        self.assignee_id = user_id

    def close(self):
        if self.status == Status.CLOSED:
            raise ValueError("Ticket is already closed")
        self.status = Status.CLOSED
        self.updated_at = _now_utc()

    def __post_init__(self):
        if not self.title:
            raise ValueError("Ticket title cannot be empty.")
