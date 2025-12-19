from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    is_agent: bool = False
    is_admin: bool = False
