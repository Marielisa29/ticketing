from dataclasses import dataclass
from datetime import datetime, timezone

from status import Status


def _now_utc() -> datetime:
    """Retourne l'heure actuelle en UTC."""
    return datetime.now(timezone.utc)


@dataclass
class Ticket:
    id: str
    title: str
    description: str
    status: Status = Status.OPEN
    creator_id: str
    assignee_id: str = None
    created_at: datetime = _now_utc()
    updated_at: datetime = _now_utc()

    def assign(self, user_id: str):
        self.assignee_id = user_id

    def __post_init__(self):
        if not self.title:
            raise ValueError("Ticket title cannot be empty.")
