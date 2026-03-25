from typing import Optional, List

from src.ports.ticket_repository import TicketRepository
from src.domain.ticket import Ticket
from .database import get_connection, close_connection
from .mappers import ticket_to_row, row_to_ticket


class SQLiteTicketRepository(TicketRepository):
    def __init__(self, db_path: str = "ticketing.db"):
        self.db_path = db_path

    def save(self, ticket: Ticket) -> Ticket:
        """
        Upsert du ticket dans la table `tickets` (INSERT OR REPLACE).
        Utilise ticket_to_row() pour obtenir un dict des champs à persister.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        row = ticket_to_row(ticket)

        cursor.execute(
            """
            INSERT OR REPLACE INTO tickets
            (id, title, description, creator_id, status, priority,
             assignee_id, project_id, created_at, updated_at, started_at, closed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row["id"],
                row["title"],
                row["description"],
                row["creator_id"],
                row["status"],
                row["priority"],
                row["assignee_id"],
                row["project_id"],
                row["created_at"],
                row["updated_at"],
                row["started_at"],
                row["closed_at"],
            ),
        )
        conn.commit()
        close_connection(conn)
        return ticket

    def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """
        Récupère une ligne depuis la table tickets par id et la convertit en Ticket.
        Retourne None si aucune ligne trouvée.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()
        close_connection(conn)

        if row is None:
            return None

        return row_to_ticket(dict(row))

    def list_all(self) -> list[Ticket]:
        """
        Récupère toutes les lignes de la table tickets et les convertit en Tickets.
        """
        conn = get_connection(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets")
        rows = cursor.fetchall()
        close_connection(conn)

        tickets: List[Ticket] = []
        for r in rows:
            tickets.append(row_to_ticket(dict(r)))
        return tickets