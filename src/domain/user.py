from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    is_agent: bool = False
    is_admin: bool = False

    def __post_init__(self):
        if not self.username:
            raise ValueError("Ticket title cannot be empty.")
