from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from src.domain.exceptions import (
    InvalidTicketStateError,
    TicketNotAssignedError,
    WrongAgentError,
)
from src.domain.priority import Priority
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
    priority: Priority = Priority.MEDIUM
    status: Status = Status.OPEN
    assignee_id: Optional[str] = None
    project_id: Optional[str] = None
    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)
    started_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    # Transitions autorisées
    ALLOWED_TRANSITIONS = {
        Status.OPEN: [Status.IN_PROGRESS],
        Status.IN_PROGRESS: [Status.RESOLVED],
        Status.RESOLVED: [Status.CLOSED, Status.IN_PROGRESS],
        Status.CLOSED: [Status.IN_PROGRESS],
    }

    def assign(self, user_id: str):
        if self.status == Status.CLOSED:
            raise ValueError("Cannot assign a closed ticket")
        self.assignee_id = user_id
        self.updated_at = _now_utc()

    def close(self):
        if self.status == Status.CLOSED:
            raise ValueError("Ticket is already closed")
        self.status = Status.CLOSED
        self.closed_at = _now_utc()
        self.updated_at = _now_utc()

    def open(self):
        """Ouvre un ticket fermé."""
        if self.status == Status.CLOSED:
            raise ValueError("Cannot open a closed ticket")
        self.status = Status.OPEN
        self.updated_at = _now_utc()

    def start(self, agent_id: str, started_at: datetime) -> None:
        """
        Démarre le traitement du ticket.

        Validations métier:
        1. Le ticket doit être assigné
        2. L'agent doit être celui assigné
        3. Le ticket doit être en statut OPEN

        Args:
            agent_id: ID de l'agent qui démarre le ticket
            started_at: Date/heure du démarrage

        Raises:
            TicketNotAssignedError: Si le ticket n'est pas assigné
            WrongAgentError: Si agent_id != assignee_id
            InvalidTicketStateError: Si le statut n'est pas OPEN
        """
        # Validation 1 : Ticket doit être assigné
        if self.assignee_id is None:
            raise TicketNotAssignedError("Ticket must be assigned before starting")

        # Validation 2 : L'agent doit être le bon
        if self.assignee_id != agent_id:
            raise WrongAgentError(
                f"Only agent {self.assignee_id} can start this ticket, not {agent_id}"
            )

        # Validation 3 : Le ticket doit être OPEN
        if self.status != Status.OPEN:
            raise InvalidTicketStateError(
                f"Ticket must be OPEN to start, current status: {self.status.value}"
            )

        # Effectuer la transition et enregistrer l'heure de démarrage
        self.transition_to(Status.IN_PROGRESS, started_at)
        self.started_at = started_at
        self.updated_at = started_at

    def _restore_status_from_db(self, status: Status) -> None:
        """
        Méthode utilitaire utilisée par les mappers/ORM pour restaurer
        le statut d'un ticket depuis la base de données.

        Cette méthode contourne certaines validations faites à la création
        (car on reconstruit un état déjà persistant). Elle doit simplement
        affecter le statut tel qu'il est dans la DB.
        """
        # On suppose que la valeur fournie est une instance de Status
        # (le mapper doit convertir la chaîne en Status avant d'appeler).
        self.status = status

    def __post_init__(self):
        # Validation des champs obligatoires
        if not self.title:
            raise ValueError("Ticket title cannot be empty.")
        if not self.description:
            raise ValueError("Ticket description cannot be empty.")
        # status doit être une instance de Status
        if not isinstance(self.status, Status):
            raise ValueError("Ticket status must be valid.")
        if self.created_at is None:  # Vérification de la date de création
            raise ValueError("Ticket creation date cannot be empty.")
        if self.updated_at is None:  # Vérification de la date de mise à jour
            raise ValueError("Ticket update date cannot be empty.")
        # priority doit être une instance de Priority
        if not isinstance(self.priority, Priority):
            raise ValueError("Ticket priority must be valid.")

    def transition_to(self, new_status: Status, updated_at: datetime) -> None:
        """Fait transiter le ticket vers un nouveau statut."""
        if new_status not in self.ALLOWED_TRANSITIONS.get(self.status, []):
            raise ValueError(
                f"Cannot transition from {self.status.value} to {new_status.value}"
            )
        self.status = new_status
        self.updated_at = updated_at
